# -*- coding:utf-8 -*-
# @FileName  : config.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 函数配置文件

import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import BasePromptTemplate
from langchain.chains import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config:
    openai_chat_model = "gpt-3.5-turbo"
    openai_16k_chat_model = "gpt-3.5-turbo-16k"
    _llm = ChatOpenAI
    # conversation_llm = OpenAI(model_name=openai_chat_model, temperature=0.5)
    stochastic_llm = _llm(model_name=openai_chat_model, temperature=0.5)
    deterministic_llm = _llm(model_name=openai_chat_model, temperature=0)
    streaming_llm = _llm(model_name=openai_chat_model, temperature=0.5, streaming=True,
                         callbacks=[StreamingStdOutCallbackHandler()])
    long_llm = _llm(model_name=openai_16k_chat_model, temperature=0)
    SESSDATA = os.getenv("SESSDATA")
    # @staticmethod
    # def create_conversation_chain(llm, prompt: BasePromptTemplate) -> ConversationChain:
    #     return ConversationChain(llm=llm, prompt=prompt, memory=ConversationBufferWindowMemory(k=5))

    @staticmethod
    def create_llm_chain(llm: BaseLanguageModel, prompt: BasePromptTemplate) -> LLMChain:
        return LLMChain(llm=llm, prompt=prompt)
