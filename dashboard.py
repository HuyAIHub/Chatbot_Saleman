import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import gradio as gr
from collections import Counter
import re
from utils.db_postgresql import DatabaseHandler
import time
import schedule
import threading

# Biến toàn cục để lưu trữ dữ liệu
global df

# Hàm upload dữ liệu từ Database
def upload():
    global df
    db_handler = DatabaseHandler()
    df = db_handler.craw_data()

    # Tiền xử lý dữ liệu
    df['created_date'] = df['created_date'].apply(parse_date)
    df['created_date'] = pd.to_datetime(df['created_date'])

# Hàm chuyển đổi định dạng ngày
def parse_date(date_str):
    if "_" in date_str:
        return pd.to_datetime(date_str, format="%Y-%m-%d_%H:%M:%S")
    else:
        return pd.to_datetime(date_str + "_00:00:00", format="%Y-%m-%d_%H:%M:%S")

# Tính số lượng User theo ngày
def calculate_daily_user_count():
    global df
    daily_user_count = df.groupby(df['created_date'].dt.date)['user_id'].nunique().reset_index()
    daily_user_count.columns = ['Day', 'Number User']
    return daily_user_count

# Hàm lấy các từ xuất hiện nhiều nhất
def get_most_common_words(text_series, top_n=50):
    words = ' '.join(text_series.dropna()).lower()
    words = re.findall(r'\b\w+\b', words)
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# Hàm tạo dữ liệu cho bảng theo khoảng thời gian
def create_date(start_week, end_week):
    global df
    df_filtered = df[(df['created_date'] >= start_week) & (df['created_date'] <= end_week)]
    session_qa_sum = df_filtered.groupby('user_id').agg(total_qa=('session_id', 'count')).reset_index()
    session_total = df_filtered.groupby('user_id').agg(total_session_id=('session_id', 'nunique')).reset_index()
    merged_df = pd.merge(session_total, session_qa_sum, on='user_id', how='left')
    sorted_session_id_counts = merged_df.sort_values(by='total_qa', ascending=False)
    return sorted_session_id_counts

# Hàm lọc và sắp xếp dữ liệu của 10 người dùng đặc biệt
def creat_user(start_week, end_week):
    global df
    df['week'] = df['created_date'].dt.isocalendar().week
    user_id_list = ["430008", "35471", "189073", "196937", "58396", "291295", "282101", "60709", "253878"]
    filtered_df = df[df['user_id'].isin(user_id_list)]
    df_filtered = filtered_df[(filtered_df['created_date'] >= start_week) & (df['created_date'] <= end_week)]
    session_qa_sum = df_filtered.groupby('user_id').agg(total_qa=('session_id', 'count')).reset_index()
    session_total = df_filtered.groupby('user_id').agg(total_session_id=('session_id', 'nunique')).reset_index()
    merged_df = pd.merge(session_total, session_qa_sum, on='user_id', how='left')
    sorted_session_id_counts = merged_df.sort_values(by='total_qa', ascending=False)
    return sorted_session_id_counts

# Hàm tạo biểu đồ
def create_plots():
    global df
    daily_user_count = calculate_daily_user_count()
    most_common_words = get_most_common_words(df['human'])
    words_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

    fig, axs = plt.subplots(1, 2, figsize=(20, 8))
    sns.barplot(x='Day', y='Number User', data=daily_user_count, palette='viridis', ax=axs[0])
    axs[0].set_title('Number User per Day')
    axs[0].set_xlabel('Day')
    axs[0].set_ylabel('Number User')
    axs[0].tick_params(axis='x', rotation=45)

    sns.barplot(x='Frequency', y='Word', data=words_df, ax=axs[1])
    axs[1].set_title('Top 50 Words Used in Human')
    axs[1].set_xlabel('Frequency')
    axs[1].set_ylabel('Word')

    plt.tight_layout()
    plt.savefig('/tmp/dashboard_plots.png')
    plt.close()
    return '/tmp/dashboard_plots.png'

def total_user(start_week, end_week):
    global df
    df_filtered = df[(df['created_date'] >= start_week) & (df['created_date'] <= end_week)]
    total_user = df_filtered['user_id'].nunique()
    res_df = pd.DataFrame({'start_date': [start_week], 'end_date' : [end_week], 'total_user': [total_user]})
    return res_df

# Tạo giao diện Gradio
def gradio_interface():
    def update_dashboard(start_date, end_date):
        sorted_summary_df = create_date(start_date, end_date)
        return sorted_summary_df
    
    def update_dashboard_1(start_date, end_date):
        sorted_user_10 = creat_user(start_date, end_date)
        return sorted_user_10
    
    def update_total_user(start_date, end_date):
        total_user_up = total_user(start_date, end_date)
        return total_user_up
    with gr.Blocks() as demo:
        gr.Markdown("### Data Dashboard and Data Table")
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Visualization Dashboard")
                plot_image = gr.Image(
                    create_plots, 
                    type='filepath', 
                    label="Dashboard"
                )
        with gr.Row():
            start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2024-08-01")
            end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", value="2024-08-30")
            update_button = gr.Button("Update Dashboard")
            
        with gr.Row():    
            with gr.Column():
                gr.Markdown("#### Top texting users")
                data_table = gr.DataFrame(
                    value=pd.DataFrame(), 
                    headers=["User ID", "Total Sessions", "Total QA"], 
                    label="User Data"
                )
                
            with gr.Column():
                gr.Markdown("#### 10 special users")
                data_table_1 = gr.DataFrame(
                    value=pd.DataFrame(), 
                    headers=["User ID", "Total Sessions", "Total QA"], 
                    label="User Data"
                )
        with gr.Row():
            gr.Markdown("#### Total user")
            data_table_2 = gr.DataFrame(
                value=pd.DataFrame(), 
                headers=["start_date","end_date","total user"], 
                )
        update_button.click(update_dashboard, inputs=[start_date, end_date], outputs=[data_table])
        update_button.click(update_dashboard_1, inputs=[start_date, end_date], outputs=[data_table_1])
        update_button.click(update_total_user, inputs=[start_date, end_date], outputs=[data_table_2])

    return demo
    
# Lập lịch tải dữ liệu
def schedule_task():
    schedule.every(5).minutes.do(upload)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    upload()  # Tải dữ liệu ngay lập tức khi khởi chạy
    threading.Thread(target=schedule_task).start()
    interface = gradio_interface()
    interface.launch(server_name="10.248.243.99", server_port=7777)
