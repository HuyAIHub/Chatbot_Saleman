import requests
import pandas as pd

data_private = "/home/aiai01/Production/Rasa_LLM_Elasticsearch_update_v3/data/DS- route Kho CNCT_20240329_134227_new.xlsx"
limit_number = 15

def get_inventory(msp,mt=None):
    print('============get_inventory============')
    url = "http://wms.congtrinhviettel.com.vn/wms-service/service/magentoSyncApiWs/getListRemainStockV2"
    if mt:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt.upper()
            }
        }
    else:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt
            }
        }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers,timeout=30)
    response_data = response.json()
    if response.status_code == 200:
        response_data = response.json()

        if len(response_data['data']) == 0:
            in_stock_out = find_stock(msp, mt)
            if len(in_stock_out) == 0:
                return "Hiện tại tôi không thể tra cứu thông tin hàng tồn kho của sản phẩm bạn đang mong muốn, xin vui lòng thử lại sau."

            return f"Hiện hàng tại {mt} đã hết. Các khu vực sau còn hàng Anh/chị hãy liên hệ các CNCT sau: \n" + '\n'.join(in_stock_out)
        
        if 'data' in response_data and response_data['data'] is not None:

            info_strings = []
            num = 0
            all_amount = 0
            for item in response_data['data']:

                amount = item["amount"] if item["amount"] is not None else ""
                goods_name = item["goodsName"] if item["goodsName"] is not None else ""
                stock_name = item["stockName"] if item["stockName"] is not None else ""
                stock_code = item["stockCode"] if item["stockCode"] is not None else ""
                # In hoặc xử lý thông tin từng mục
                if stock_name != '' or stock_code !='':
                    all_amount += amount
                    if num <= limit_number:
                        info_string = (
                            f"Tên Kho: {stock_name}\n"
                            f"Mã kho: {stock_code}\n"
                            f"SL: {int(amount)}\n"
                            "       -------------------      "
                        )
                        info_strings.append(info_string)
                    num += 1
                # Kết hợp các chuỗi thành một chuỗi duy nhất
            print('all_amount:',all_amount)
            final_string = "\n".join(info_strings)
            print('----get_inventory ok------')
            return final_string
    else:
        # In lỗi nếu có
        return "Hiện tại tôi không thể tra cứu thông tin hàng tồn kho của sản phẩm bạn đang mong muốn, xin vui lòng thử lại sau."

def find_stock(msp, mt):
    print('============find_stock============')
    df = pd.read_excel(data_private)
    fil_df = df[df["origin_CNCT"].str.lower() == mt.lower()]
    sorted_df = fil_df.sort_values(by=["distanceMeters"])
    stock = []
    # find 5 stock remain good
    for index, row in sorted_df.iterrows():
        destination_CNCT = row["destination_CNCT"]
        has_stock = in_stock(msp, destination_CNCT)
        outtext = ""
        if isinstance(has_stock, str):
            # outtext = "+ + + + + + + + + + + + +"
            outtext += "\n+ + + CNCT: " + destination_CNCT + " + + +\n"
            outtext += has_stock + "\n"
            stock.append(outtext)
            if len(stock) >= 25:
                break
    return stock

def in_stock(msp, mt):
    # print('============in_stock============')
    url = "http://wms.congtrinhviettel.com.vn/wms-service/service/magentoSyncApiWs/getListRemainStockV2"

    if mt:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt.upper()
            }
        }
    else:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt
            }
        }
    # Headers nếu có (ở đây để trống nếu không yêu cầu)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers,timeout=30)
    if response.status_code == 200:
        response_data = response.json()
        
        if len(response_data['data']) == 0:
            return 0
        if 'data' in response_data and response_data['data'] is not None:
            info_strings = []
            all_amount = 0
            num = 0
            for i, item in enumerate(response_data['data']):
                # Xử lý từng mục trong danh sách
                amount = item["amount"] if item["amount"] is not None else ""
                goods_name = item["goodsName"] if item["goodsName"] is not None else ""
                stock_name = item["stockName"] if item["stockName"] is not None else ""
                stock_code = item["stockCode"] if item["stockCode"] is not None else ""
                # In hoặc xử lý thông tin từng mục
                if stock_name != '' or stock_code !='':
                    all_amount += int(amount)
                    if num <= 5:
                        info_string = (
                            f"{i+1}. {stock_name}\n"
                            f"Mã kho: {stock_code}\n"
                            f"SL: {int(amount)}\n"
                            "      -------------------     "
                        )
                        info_strings.append(info_string)
                    num += 1
                # Kết hợp các chuỗi thành một chuỗi duy nhất
            print('mt:',mt)
            print('all_amount:',all_amount)
            final_string = "\n".join(info_strings)
            print('----in_stock ok------')
            return final_string
    else:
        print('----in_stock ok------')
        # In lỗi nếu có
        return "Hiện tại tôi không thể tra cứu thông tin hàng tồn kho của sản phẩm bạn đang mong muốn, xin vui lòng thử lại sau.\n"

def multi_get(ma, mt):
    product = ""
    print("------ma------", ma)
    masp = ma.strip().split(",")
    print(masp)
    for i, msp in enumerate(masp):
        print(msp)
        outtext = f"- Với mã/tên sản phẩm {msp}: \n"
        get_msp = get_inventory(msp.strip(), mt)

        outtext += get_msp
        product += outtext + "\n"
    return product
# print(multi_get('adafef','HNI'))
# print(get_inventory('M&Egd000217','hpg'))
