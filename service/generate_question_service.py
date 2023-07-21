# -*- coding:utf-8 -*-
# @FileName  : generate_question_service.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 题目生成业务模块

import gradio as gr
from utils.question_assistant import QuestionAssistant
from utils.cache_handler import CacheHandler
from entity.question_result import ChoiceQuestionResult, ShortAnswerQuestionResult


def generate_question(question_type: str, desc: str, subject: str):
    """
    生成题目
    :param question_type: 题目类型
    :param desc: 题目描述
    :param subject: 科目

    """
    question_assistant = QuestionAssistant()
    question = "题目获取失败"
    if question_type == "选择题":
        result = question_assistant.generate_choice_question(desc, subject)
        question = ChoiceQuestionResult.get_choice_question(result)["question"]
    if question_type == "简答题":
        result = question_assistant.generate_short_answer_question(desc, subject)
        question = ShortAnswerQuestionResult.get_short_answer_question(result)["question"]

    return gr.update(value=question)


def remove_question(question: str, subject_type: str):
    if question:
        cache_handler = CacheHandler()
        cache_handler.pop_question(subject_type)
        return gr.update(value="")
    else:
        raise gr.Error("移除失败")
