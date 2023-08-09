# -*- coding:utf-8 -*-
# @FileName  : config.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 函数配置文件

import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import BasePromptTemplate
from langchain.chains import LLMChain
from common.ernie_bot import ErnieBot


def get_openai_proxy():
    return os.getenv("OPENAI_API_PROXY")


def get_access_info():
    return os.getenv("ACCESS_INFO")


class Config:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        os.environ["OPENAI_API_KEY"] = "sk"

    def get_llm(self):
        llm = self._get_model()
        return llm

    @staticmethod
    def get_SESSDATA():
        return os.getenv("SESSDATA")

    @staticmethod
    def create_llm_chain(llm, prompt: BasePromptTemplate) -> LLMChain:
        return LLMChain(llm=llm, prompt=prompt)

    @staticmethod
    def _get_model():
        model = os.getenv("MODEL")
        if model is None:
            raise ValueError("MODEL is not set")
        if model == "openai":
            return ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.5,
                openai_api_key=get_access_info(),
                openai_api_base=get_openai_proxy())
        if model == "ernie":
            return ErnieBot()
        print(os.getenv("ACCESS_INFO"))