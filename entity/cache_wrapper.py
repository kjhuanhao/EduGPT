# -*- coding:utf-8 -*-
# @FileName  : cache_wrapper.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 缓存的包装类

import json

from entity.subject import SubjectType
from typing import List, Dict
from entity.question_result import QuestionResult, ShortAnswerQuestionResult


class CacheQuestionWrapper:
    """
    缓存题目的包装类
        a = {
        "Chinese": [],
        "Math": [],
        "English": [],
        "Physics": [],
        "Chemistry": [],
        "Biology": [],
        "History": [],
        "Geography": [],
        "Politics": [] }

    """

    def __init__(self, my_dict: Dict):
        self._data = my_dict

    def get_value(self, key):
        return self._data.get(key)

    def set_value(self, key, value: List):
        if SubjectType.validate_subject_type(key):
            self._data[key] = value

    def get_keys(self):
        return list(self._data.keys())

    def get_items(self):
        return list(self._data.items())
