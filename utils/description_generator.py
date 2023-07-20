# -*- coding:utf-8 -*-
# @File      : description_generator.py
# @Time      : 2023/7/18
# @Author    : LinZiHao
# @Desc      : 生成题目
import os

from utils.question_assistant import QuestionAssistant
from utils.cache_handler import CacheHandler
from typing import Optional, Union
from prompt.structured_prompt import DESCRIPTION_PROMPT
from entity.question_result import ChoiceQuestionResult, ShortAnswerQuestionResult

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts import BasePromptTemplate


class DescriptionGenerator:
    def __init__(self,
                 title: str,
                 llm: Optional[BaseLanguageModel] = None,
                 ):
        self.target_title = title
        self._handler = StreamingStdOutCallbackHandler()
        if llm is None:
            llm = ChatOpenAI(model_name=os.getenv("CHAT_MODEL"),
                             temperature=0,
                             callbacks=[self._handler],
                             streaming=True
                             )
        self._llm = llm
        self._description_chain = self._create_llm_chain(llm=self._llm, prompt=DESCRIPTION_PROMPT)
        self._cache_handler = CacheHandler()

    def generate_question_from_video(self,
                                     subject_type: str,
                                     question_type: Union[ChoiceQuestionResult, ShortAnswerQuestionResult], ):
        if isinstance(question_type, ChoiceQuestionResult):
            question = QuestionAssistant().generate_choice_question(self.generate_description(),
                                                                    subject_type)
        else:
            question = QuestionAssistant().generate_short_answer_question(self.generate_description(),
                                                                          subject_type)
        return question

    def get_summary_text_cache(self) -> None:
        """
        获取缓存的字幕总结
        :return:
        """
        info = self._cache_handler.get_subtitle_cache()
        for dictionary in info:
            if "title" in dictionary and dictionary['title'] == self.target_title:
                return dictionary.get('summary')
        raise KeyError(f"未找到指定的 title 键值对")

    def generate_description(self, description_num: Optional[int] = None):
        description_num = 3 if description_num is None else description_num
        desc = self._description_chain.run(
            description_num=description_num,
            text=self.get_summary_text_cache()
        )
        return desc

    @staticmethod
    def _create_llm_chain(llm, prompt: BasePromptTemplate):
        return LLMChain(llm=llm, prompt=prompt)
