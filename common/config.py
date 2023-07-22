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


def get_openai_proxy():
    return os.getenv("OPENAI_API_PROXY")


def get_openai_key():
    return os.getenv("OPENAI_API_KEY")


class Config:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        os.environ["OPENAI_API_KEY"] = "sk"

    openai_chat_model = "gpt-3.5-turbo"
    openai_16k_chat_model = "gpt-3.5-turbo-16k"

    @staticmethod
    def get_SESSDATA():
        return os.getenv("SESSDATA")

    @staticmethod
    def get_stochastic_llm():
        print(get_openai_key())
        return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, openai_api_key=get_openai_key(), openai_api_base=get_openai_proxy())

    @staticmethod
    def get_deterministic_llm():
        return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=get_openai_key(), openai_api_base=get_openai_proxy())

    @staticmethod
    def get_long_llm():
        return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=get_openai_key(), openai_api_base=get_openai_proxy())

    @staticmethod
    def create_llm_chain(llm: BaseLanguageModel, prompt: BasePromptTemplate) -> LLMChain:
        return LLMChain(llm=llm, prompt=prompt)
