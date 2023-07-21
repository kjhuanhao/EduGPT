# -*- coding:utf-8 -*-
# @FileName  : brush_questions_service.py
# @Time      : 2023/7/18
# @Author    : LaiJiahao
# @Desc      : 刷题业务模块

import gradio as gr
from utils.cache_handler import CacheHandler
import random


def update_question_info(local_state, subject_type: str):
    cache_handler = CacheHandler()
    all_questions = cache_handler.get_question_cache()
    subject_questions = all_questions[subject_type]
    if len(subject_questions) == 0:
        raise gr.Error("题库中没有该科目的题目，请进行生成")
    else:
        list_length = len(subject_questions)
        random_index = random.randint(0, list_length - 1)
        subject_question = subject_questions[random_index]
    # 对题目类型进行判断
    question = subject_question["question"]
    clue = subject_question["clue"]
    answer = subject_question["answer"]
    explanation = subject_question["explanation"]
    local_state["clue"] = "提示:\n" + clue
    local_state["answer_explanation"] = f"答案:\n {answer} \n \n 解释:\n{explanation} "

    if subject_question["type"] == "choice":
        options = [value for value in subject_question["options"].values()]
        return [gr.update(choices=options, visible=True),  # 选择题更新选项
                gr.update(visible=False),  # 简答题不更新选项
                gr.update(value=question),
                gr.update(value=local_state)]
    if subject_question["type"] == "short_answer":
        return [gr.update(visible=False),  # 选择题不更新选项
                gr.update(visible=True),  # 简答题更新
                gr.update(value=question),
                gr.update(value=local_state)]
