# -*- coding:utf-8 -*-
# @File      : description_generator.py
# @Time      : 2023/7/18
# @Author    : LinZiHao
# @Desc      : 生成题目

from utils.question_assistant import QuestionAssistant
from utils.cache_handler import CacheHandler
from typing import Optional, Union
from prompt.structured_prompt import DESCRIPTION_PROMPT
from entity.question_result import ChoiceQuestionResult, ShortAnswerQuestionResult
from common.config import Config
from langchain.chains import LLMChain
from langchain.prompts import BasePromptTemplate


@DeprecationWarning
class DescriptionGenerator:
    def __init__(self, course_id: str):
        self.course_id = course_id
        self._llm = Config.stochastic_llm
        self._description_chain = Config.create_llm_chain(self._llm, DESCRIPTION_PROMPT)
        self._cache_handler = CacheHandler()

    def generate_question_from_video(
            self,
            subject_type: str,
            question_type: Union[ChoiceQuestionResult, ShortAnswerQuestionResult]
    ):
        if isinstance(question_type, ChoiceQuestionResult):
            question = QuestionAssistant().generate_choice_question(self.generate_description(),
                                                                    subject_type)
        else:
            question = QuestionAssistant().generate_short_answer_question(self.generate_description(),
                                                                          subject_type)
        return question

    def _get_summary_text_cache(self) -> None:
        """
        获取缓存的字幕总结
        :return:
        """
        summary_text = None
        info = self._cache_handler.get_subtitle_cache()
        for course_info in info:
            for course_id in course_info:
                if course_id == self.course_id:
                    summary_text = course_info[course_id].get("summary_text")
                    return summary_text
        if summary_text is None:
            raise KeyError(f"未找到指定的 title 键值对")

    def generate_description(self, description_num: Optional[int] = None):
        description_num = 3 if description_num is None else description_num
        desc = self._description_chain.run(
            description_num=description_num,
            text=self._get_summary_text_cache()
        )
        return desc

    @staticmethod
    def _create_llm_chain(llm, prompt: BasePromptTemplate):
        return LLMChain(llm=llm, prompt=prompt)
