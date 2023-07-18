# -*- coding:utf-8 -*-
# @FileName  : initialize.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 初始化app的state状态

from typing import Dict
from utils.cache_handler import CacheHandler


def initialize_state() -> Dict:
    """
    初始化app的state状态，这里放入组件需要的预加载的数据
    已存入的数据:
        1. 所有的科目类型

    """
    state = {}
    cache_handler = CacheHandler()
    # question_cache = cache_handler.get_question_cache()
    # state["question_cache"] = question_cache
    state["subject_types"] = cache_handler.subject_types
    return state

