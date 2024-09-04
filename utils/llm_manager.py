import logging, time
from langchain_community.chat_models import ChatOpenAI
from config_app.config import get_config
from langchain_groq import ChatGroq
from openai import OpenAI
import openai
import requests
# Cấu hình logging
import logging
import os
from groq import Groq

config_app = get_config()
openai_api_key = config_app['parameter']['openai_api_key']
    
def get_llm():
    return ChatOpenAI(model_name=config_app["parameter"]["gpt_model_to_fewshot"], openai_api_key=openai_api_key, temperature=config_app["parameter"]["temperature"])

def gen_llm():
    return ChatOpenAI(model_name=config_app["parameter"]["gpt_model_to_gen"], openai_api_key=openai_api_key, temperature=config_app["parameter"]["temperature"], max_tokens=config_app["parameter"]["max_tokens"])
# print(get_llm())