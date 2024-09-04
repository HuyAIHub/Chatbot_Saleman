import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, UploadFile, Form, File
from config_app.config import get_config
from main_run import handle_request
import datetime, os
from logs.log_file import Logger_Days
config_app = get_config()

app = FastAPI()
numberrequest = 0

@app.post('/llm')
async def post(
    InputText: str = Form(None),
    IdRequest: str = Form(...),
    NameBot: str = Form(...),
    User: str = Form(...),
    GoodsCode: str = Form(None),
    ProvinceCode: str = Form(None),
    ObjectSearch: str = Form(None),
    PriceSearch: str = Form(None),
    DescribeSearch: str = Form(None),
    Image: UploadFile = File(None),
    Voice: UploadFile = File(None)
):
    global numberrequest
    numberrequest += 1
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    logging = Logger_Days(f"./logs/logchatbot/logchatbot_{str(config_app['server']['port'][7])}" + '_' + current_date)

    logging.info("----------------NEW_SESSION--------------")
    logging.info(f"InputText: {InputText}")
    print("----------------NEW_SESSION--------------")
    print("NumberRequest", numberrequest)
    print("User  = ", User)
    print("InputText  = ", InputText)
    results = handle_request(
                        InputText=InputText,
                        IdRequest=IdRequest,
                        NameBot=NameBot,
                        User=User,
                        GoodsCode=GoodsCode,
                        ProvinceCode=ProvinceCode,
                        ObjectSearch=ObjectSearch, 
                        PriceSearch=PriceSearch,
                        DescribeSearch=DescribeSearch,
                        Image=Image,
                        Voice=Voice
                        )
    return results


uvicorn.run(app, host="0.0.0.0", port=config_app['server']['port'][7])