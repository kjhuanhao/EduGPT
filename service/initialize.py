# -*- coding:utf-8 -*-
# @FileName  : initialize.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 初始化app的state状态

import os
from typing import Dict
from utils.cache_handler import CacheHandler
from entity.toolkit import Toolkit
import gradio as gr


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


def set_env(model, access_info, bilibili_SESSDATA, proxy_url):
    """
    设置环境变量
    """
    if not access_info:
        return gr.update(value="⚠️状态：设置失败，鉴权信息为空")
    os.environ["MODEL"] = model
    os.environ["OPENAI_API_PROXY"] = proxy_url
    os.environ["ACCESS_INFO"] = access_info
    os.environ["SESSDATA"] = bilibili_SESSDATA

    return gr.update(value="✅状态：设置环境变量成功")
