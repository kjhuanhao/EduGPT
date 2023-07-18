# -*- coding:utf-8 -*-
# @FileName  : structured_prompt.py
# @Time      : 2023/7/15
# @Author    : LaiJiahao
# @Desc      : 结构化prompt

from langchain.prompts.prompt import PromptTemplate


from prompt.analyzer_prompt import PLOT_PROMPT_TEMPLATE
from prompt.summary_prompt import SUMMARY_TEMPLATE
from prompt.question_prompt import (
    QUESTION_CHOICE_TEMPLATE,
    QUESTION_SHORT_ANSWER_TEMPLATE,
    VERIFY_ANSWER_TEMPLATE
)

# 绘制的prompt
PLOT_PROMPT = PromptTemplate(
    input_variables=["columns", "example", "file_path", "instruction"], template=PLOT_PROMPT_TEMPLATE
)

# 总结字幕的prompt
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summary_count", "subtitle"], template=SUMMARY_TEMPLATE
)

# 单选题的prompt
QUESTION_CHOICE_PROMPT = PromptTemplate(
    input_variables=["instruction", "subject"], template=QUESTION_CHOICE_TEMPLATE
)


# 简答题的prompt
QUESTION_SHORT_ANSWER_PROMPT = PromptTemplate(
    input_variables=["instruction", "subject"], template=QUESTION_SHORT_ANSWER_TEMPLATE
)

# 验证简答题的prompt
VERIFY_ANSWER_PROMPT = PromptTemplate(
    input_variables=["question", "answer"], template=VERIFY_ANSWER_TEMPLATE
)