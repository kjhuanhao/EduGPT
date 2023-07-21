# -*- coding:utf-8 -*-
# @FileName  : initialize.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 初始化app的state状态

import os
from typing import Dict
from utils.cache_handler import CacheHandler
from entity.toolkit import Toolkit
from dotenv import load_dotenv, find_dotenv
import gradio as gr

load_dotenv(find_dotenv())


def initialize_state() -> Dict:
    """
    初始化app的state状态，这里放入组件需要的预加载的数据
    已存入的数据:
        1. 所有的科目类型
        2. 所有的插件
    """
    state = {}
    cache_handler = CacheHandler()
    # question_cache = cache_handler.get_question_cache()
    # state["question_cache"] = question_cache
    cache_handler = CacheHandler()

    state["subject_types"] = cache_handler.subject_types
    state["plugins"] = [value.value for value in list(Toolkit)]

    return state


def check_settings():
    api_key = os.getenv("OPENAI_API_KEY")
    bilibili_SESSDATA = os.getenv("SESSDATA")
    return [gr.update(value=lambda: api_key is not None),
            gr.update(value=lambda: bilibili_SESSDATA is not None)]
