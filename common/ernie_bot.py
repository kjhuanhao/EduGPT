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


