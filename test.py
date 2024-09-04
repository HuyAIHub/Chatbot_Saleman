import requests

# url = "https://apis-public.congtrinhviettel.com.vn/llm"
url = "http://10.248.243.99:8099/llm"
data = {
    "InputText": "loại máy giặt nào tốt nhất bên bạn",
    "IdRequest": "9007974189",
    "NameBot": "ChatBot",
    "User": "282101",
    "GoodsCode": "",
    "ProvinceCode": "",
    "ObjectSearch": "",
    "PriceSearch": "",
    "DescribeSearch": "",
}

response = requests.post(url, data=data)
print(response.json())

# import os
# import logging
# from fastapi import FastAPI, Form, File, UploadFile
# import asyncio, uvicorn
# import time
# app = FastAPI()
# numberrequest = 0

# # Asynchronous function to handle requests
# async def handle_request(
#     InputText=None,
#     IdRequest=None,
#     NameBot=None,
#     User=None,
#     GoodsCode=None,
#     ProvinceCode=None,
#     ObjectSearch=None,
#     PriceSearch=None,
#     DescribeSearch=None,
#     Image=None,
#     Voice=None
#     ):
#     # Simulate processing time (replace with actual logic)
#     # time.sleep(5)  # Simulate some async work
#     await asyncio.sleep(5)
#     return {"status": "success", "InputText": InputText, "User": User}

# @app.post('/llm')
# async def post(
#     InputText: str = Form(None),
#     IdRequest: str = Form(...),
#     NameBot: str = Form(...),
#     User: str = Form(...),
#     GoodsCode: str = Form(None),
#     ProvinceCode: str = Form(None),
#     ObjectSearch: str = Form(None),
#     PriceSearch: str = Form(None),
#     DescribeSearch: str = Form(None),
#     Image: UploadFile = File(None),
#     Voice: UploadFile = File(None)
# ):
#     global numberrequest
#     numberrequest += 1
   
#     # Handle request asynchronously
#     results = await handle_request(
#                         InputText=InputText,
#                         IdRequest=IdRequest,
#                         NameBot=NameBot,
#                         User=User,
#                         GoodsCode=GoodsCode,
#                         ProvinceCode=ProvinceCode,
#                         ObjectSearch=ObjectSearch, 
#                         PriceSearch=PriceSearch,
#                         DescribeSearch=DescribeSearch,
#                         Image=Image,
#                         Voice=Voice
#                         )
#     return results
# if __name__ == "__main__":
#     uvicorn.run("test:app", host="0.0.0.0", port=1113, workers=4, log_level="debug")

# # gunicorn -w 4 -k uvicorn.workers.UvicornWorker test:app --threads 2 --worker-connections 100 --host 0.0.0.0 --port 1113
# # uvicorn test:app --workers 4 --limit-concurrency 20 --host 0.0.0.0 --port 1113
# # uvicorn test:app --workers 4 --limit-concurrency 20 --host 0.0.0.0 --port 1113 --log-level debug

# import requests
# from rag_architecture.retrieval import search_db
# # url = "https://apis-public.congtrinhviettel.com.vn/llm"
# url = "http://10.248.243.99:8099/llm"
# file_dir = "/home/aiai01/Production/Rasa_LLM_Elasticsearch_update_v3/data/images/dieuhoa.jpg"

# data = {
#     "InputText": "điều hòa",
#     "IdRequest": "123",
#     "NameBot": "vbot",
#     "User": "123",
#     "GoodsCode": "",
#     "ProvinceCode": "",
#     "ObjectSearch": "",
#     "PriceSearch": "",
#     "DescribeSearch": ""
# }
# files = {
#     "Image": open(file_dir, "rb")
# }
# # # import requests
# import time

# t1 = time.time()
# # for i in range(100):
#     # demand = {"object": ["điều hòa"]}
#     # messsage, product, ok = search_db(demand)
# response = requests.post(url, data=data)
# print(response.json())
# print("=====time total=====", time.time()-t1)
    # - Nếu thông tin không có trong dữ liệu xin hãy trả lời: "Hiện tại tôi không có thông tin về sản phẩm này. Anh/chị cho tôi biết cần sản phẩm nào? Có tầm giá bao nhiêu? Tôi sẽ giúp Anh/chị tìm kiếm. Cảm ơn Anh/chị."

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker test:app --threads 2 --worker-connections 100 --host 0.0.0.0 --port 1113
# uvicorn test:app --workers 4 --limit-concurrency 20 --host 0.0.0.0 --port 1113
# uvicorn test:app --workers 4 --limit-concurrency 20 --host 0.0.0.0 --port 1113 --log-level debug