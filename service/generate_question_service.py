# -*- coding:utf-8 -*-
# @FileName  : generate_question_service.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 题目生成业务模块

import gradio as gr
from utils.question_assistant import QuestionAssistant


def generate_question(question_type: str, desc: str, subject: str):
    """
    生成题目
    :param question_type: 题目类型
    :param desc: 题目描述
    :param subject: 科目

    """
    question_assistant = QuestionAssistant()
    if question_type == "选择题":
        result = question_assistant.generate_choice_question(desc, subject)
        question = result.get_choice_question().get("question")
        return gr.update(value=question)
    if question_type == "简答题":
        result = question_assistant.generate_short_answer_question(desc, subject)
        question = result.get_short_answer_question().get("question")
        return gr.update(value=question)
