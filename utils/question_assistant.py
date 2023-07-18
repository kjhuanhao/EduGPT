# -*- coding:utf-8 -*-
# @FileName  : question_assistant.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : 设置题目

import os

from loguru import logger
from typing import Optional, Dict
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import BasePromptTemplate
from langchain.chains import LLMChain
from prompt.structured_prompt import (
    QUESTION_CHOICE_PROMPT,
    QUESTION_SHORT_ANSWER_PROMPT,
    VERIFY_ANSWER_PROMPT
)
from entity.subject import SubjectType
from entity.question_result import ChoiceQuestionResult, ShortAnswerQuestionResult
from utils.cache_handler import CacheHandler


class QuestionAssistant:

    def __init__(
            self,
            llm: Optional[BaseLanguageModel] = None,
    ) -> None:
        if llm is None:
            llm = ChatOpenAI(model_name=os.getenv("CHAT_MODEL"),
                             temperature=0.5,
                             )
        self._llm = llm
        self._set_choice_question_chain = self._create_llm_chain(prompt=QUESTION_CHOICE_PROMPT)
        self._set_short_answer_question_chain = self._create_llm_chain(prompt=QUESTION_SHORT_ANSWER_PROMPT)
        self._verify_answer_chain = self._create_llm_chain(prompt=VERIFY_ANSWER_PROMPT)
        self._cache_handler = CacheHandler()

    def generate_choice_question(self, desc: str, subject_type: str) -> ChoiceQuestionResult:
        """
        生成选择题
        :param desc: 题目描述
        :param subject_type: 科目
        :return: 选择题的字典

        """
        logger.info("正在生成选择题")
        response = self._set_choice_question_chain.run(
            instruction=desc,
            subject=SubjectType.get(subject_type)
        )
        choice_question_result = ChoiceQuestionResult(response)
        logger.info("选择题生成完毕")
        self._cache_handler.question_cache(subject_type, choice_question_result)
        return choice_question_result

    def generate_short_answer_question(self, desc: str, subject_type: str) -> ShortAnswerQuestionResult:
        """
        生成简答题
        :param desc: 题目描述
        :param subject_type: 科目
        :return: 简答题的字典

        """
        logger.info("正在生成简答题")
        response = self._set_short_answer_question_chain.run(
            instruction=desc,
            subject=SubjectType.get(subject_type)
        )
        short_answer_result = ShortAnswerQuestionResult(response)
        logger.info("简答题生成完毕")
        self._cache_handler.question_cache(subject_type, short_answer_result)
        return short_answer_result

    def verify_question(self, question: str, answer: str):
        """
        验证答案
        :param question: 题目
        :param answer: 答案
        :return: None

        """
        logger.info("正在验证答案")
        self._verify_answer_chain.run(
            question=question,
            answer=answer
        )

    def _create_llm_chain(self, prompt: BasePromptTemplate):
        return LLMChain(llm=self._llm, prompt=prompt)
