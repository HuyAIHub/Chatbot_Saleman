from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate
)
from config_app.enum import Variable
from langchain_community.callbacks import get_openai_callback
from utils.llm_manager import gen_llm
from config_app.config import get_config
import re
config_app = get_config()
enum = Variable()
memories = {}
llm = gen_llm()
def get_memory(session_id):
    if session_id not in memories:
        memories[session_id] = ConversationBufferWindowMemory(k = config_app["parameter"]["search_number_messages"],
                                                              return_messages=True)
        memories[session_id].memory_key = session_id
    return memories[session_id]

def output(chain, human_input):
    # print('====initialize_chat_conversation====', chain, memory, human_input)
    total_tokens = ''
    response = None
    try: 
        with get_openai_callback() as cb:
            response = chain.predict(human_input=human_input)
            total_tokens = cb.total_tokens
            print('======total_tokens=====\n', cb.total_tokens)
    except Exception as e:
        print(f"An error occurred during prediciton: {e}")

    return response,total_tokens

def initialize_chat_conversation(human_input, response_elastic, session_id):
    # print('====initialize_chat_conversation====', human_input,response_elastic, session_id,llm)
    memory = get_memory(session_id)
    prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=enum.SYSTEM_MESSAGE
        ),
        MessagesPlaceholder(
            variable_name=session_id
        ),
        HumanMessagePromptTemplate.from_template(
            enum.HUMAN_MESSAGE_TEMPLATE
        ),
    ]
    )

    prompt.messages[0].content = prompt.messages[0].content.format(context=response_elastic)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        # verbose=True,
        memory=memory
    )
    response, total_tokens = output(chain, human_input)
    
    return response, memory, total_tokens