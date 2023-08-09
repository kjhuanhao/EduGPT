# -*- coding:utf-8 -*-
# @FileName  : ernie_bot.py
# @Time      : 2023/8/7
# @Author    : LaiJiahao
# @Desc      : 文心一言

import json
import requests
import os

from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import openai


class ErnieBot(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        return self._get_completion(content=prompt)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"access_token":  os.getenv("ACCESS_INFO")}

    def _get_completion(self, content: str) -> str:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + os.getenv("ACCESS_INFO")

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json().get("result")
        return result

#
# prompt = "请你帮我指定一个{subject}科目的学习计划"
# template = PromptTemplate(input_variables=["subject"], template=prompt)
# chain = LLMChain(llm=ErnieBot(), prompt=template)
# print(chain.run(subject="数学"))

# access_token = "24.8d58a0f93757871f2b6eddaabebbe630.2592000.1694010538.282335-37334268"
# llm = ErnieBot()
# print(llm("你好"))
