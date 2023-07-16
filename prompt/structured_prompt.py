# -*- coding:utf-8 -*-
# @FileName  : structured_prompt.py
# @Time      : 2023/7/15
# @Author    : LaiJiahao
# @Desc      : 结构化prompt

from langchain.prompts.prompt import PromptTemplate
from prompt.analyzer_prompt import PLOT_PROMPT_TEMPLATE
from prompt.summary_prompt import SUMMARY_TEMPLATE

# 绘制的prompt
PLOT_PROMPT = PromptTemplate(
    input_variables=["columns", "example", "explanation", "instruction"], template=PLOT_PROMPT_TEMPLATE
)

# 总结字幕的prompt
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summary_count", "subtitle"], template=SUMMARY_TEMPLATE
)
