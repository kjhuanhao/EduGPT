# -*- coding:utf-8 -*-
# @FileName  : cache_handler.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 缓存处理

import os
import json

from loguru import logger
from typing import Dict, Union, List
from entity.question_result import ChoiceQuestionResult, ShortAnswerQuestionResult
from entity.subject import SubjectType


class CacheHandler:
    _OUTPUT_fOLDER = "cache/"
    _ANALYZER_FILE = "analyzer.json"
    _QUESTION_FILE = "question.json"
    _SUBTITLE_FILE = "subtitle.json"
    _ANALYZER_PATH = _OUTPUT_fOLDER + _ANALYZER_FILE
    _QUESTION_PATH = _OUTPUT_fOLDER + _QUESTION_FILE
    _SUBTITLE_PATH = _OUTPUT_fOLDER + _SUBTITLE_FILE

    def __init__(self):
        """
        初始化缓存处理，从本地读取缓存
        """
        if not os.path.exists(self._OUTPUT_fOLDER):
            os.makedirs(self._OUTPUT_fOLDER)
        self.subject_types = [value.name for value in list(SubjectType)]

    def analyzer_cache(self, cache_message: Dict) -> None:
        if os.path.isfile(self._ANALYZER_PATH):
            with open(self._ANALYZER_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        existing_data.append(cache_message)

        with open(self._ANALYZER_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f)

        logger.info("缓存结束")

    def question_cache(
            self,
            subject_type: str,
            question_result: Union[ChoiceQuestionResult, ShortAnswerQuestionResult]
    ) -> None:
        """
        将题目进行缓存
        :return: None
        """
        if not SubjectType.validate_subject_type(subject_type):
            return
        logger.info("读取本地题库缓存")

        existing_data = self.get_question_cache()

        logger.info("开始缓存题目")

        if isinstance(question_result, ChoiceQuestionResult):
            result = question_result.get_choice_question()
        else:
            result = question_result.get_short_answer_question()

        existing_data[subject_type].append(result)

        with open(self._QUESTION_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f)
        logger.info("题目缓存结束")

    def get_question_cache(self) -> Dict:
        """
        获取缓存的题目
        :return: 题目
        """
        if os.path.isfile(self._QUESTION_PATH):
            with open(self._QUESTION_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)  # 将json文件转换为字典
        else:
            existing_data = {item: [] for item in self.subject_types}

        return existing_data

    def pop_question(self, subject_type):
        """
        移除最后一个问题
        """
        logger.info("操作删除问题")
        question_cache = self.get_question_cache()
        subject_questions = question_cache[subject_type]
        subject_questions.pop()
        question_cache[subject_type] = subject_questions
        with open(self._QUESTION_PATH, 'w', encoding='utf-8') as f:
            json.dump(question_cache, f)

    def subtitle_cache(self, b_cid: str, title: str, subtitle: str, summary: str) -> Dict:
        """
        将标题、字幕、字幕总结进行缓存
        :return: None
        """
        logger.info("读取本地字幕缓存")

        existing_data = self.get_subtitle_cache()

        logger.info("开始缓存字幕")

        result = {b_cid: {"title": title, "subtitle": subtitle, "summary": summary}}
        existing_data.append(result)

        with open(self._SUBTITLE_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f)
        logger.info("题目缓存结束")
        return {
            "title": title,  # 视频标题
            "subtitle": subtitle,  # 字幕内容
            "summary": summary  # 字幕总结
        }

    def get_subtitle_cache(self) -> List:
        """
        获取缓存的标题、字幕、字幕总结
        :return: 标题、字幕、字幕总结
        """
        if os.path.isfile(self._SUBTITLE_PATH):
            with open(self._SUBTITLE_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)  # 将json文件转换为列表
        else:
            existing_data = []
            with open(self._SUBTITLE_PATH, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f)

        return existing_data

    def get_summary_cache_byId(self, b_cid: str) -> str:
        """
        根据b_cid获取字幕总结
        :return: 字幕总结
        """
        for data in self.get_subtitle_cache():
            if b_cid in data:
                matching_dict = data[b_cid]
                return matching_dict["summary"]

    def judge_subtitle_cache(self, b_cid: str):
        for data in self.get_subtitle_cache():
            if b_cid in data:
                matching_dict = data[b_cid]
                return matching_dict

