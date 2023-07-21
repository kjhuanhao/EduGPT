# -*- coding:utf-8 -*-
# @FileName  : structured_prompt.py
# @Time      : 2023/7/15
# @Author    : LaiJiahao
# @Desc      : 结构化prompt

from langchain.prompts.prompt import PromptTemplate
from prompt.analyzer_prompt import PLOT_PROMPT_TEMPLATE
from prompt.summary_prompt import SUMMARY_TEMPLATE, DESCRIPTION_TEMPLATE, QA_TEMPLATE
from prompt.question_prompt import (
    QUESTION_CHOICE_TEMPLATE,
    QUESTION_SHORT_ANSWER_TEMPLATE,
    VERIFY_ANSWER_TEMPLATE,
    VIDEO_QUESTION_CHOICE_TEMPLATE,
    VIDEO_QUESTION_SHORT_ANSWER_TEMPLATE
)
from prompt.plugins_prompt import (
    STUDY_PLAN_TEMPLATE,
    CHINESE_ESSAY_SCORING_TEMPLATE,
    VIDEO_RECOMMENDATION_TEMPLATE,
    INSPIRATION_TEMPLATE
)

# 绘制的prompt
PLOT_PROMPT = PromptTemplate(
    input_variables=["columns", "example", "file_path", "instruction"], template=PLOT_PROMPT_TEMPLATE
)

# 总结字幕的prompt
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summary_count", "subtitle"], template=SUMMARY_TEMPLATE
)

# 总结描述主题的prompt
DESCRIPTION_PROMPT = PromptTemplate(
    input_variables=["description_num", "text"], template=DESCRIPTION_TEMPLATE
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

# 制定学习计划的prompt
STUDY_PLAN_PROMPT = PromptTemplate(
    input_variables=["instruction"], template=STUDY_PLAN_TEMPLATE
)

# 作文评分的prompt
CHINESE_ESSAY_SCORING_PROMPT = PromptTemplate(
    input_variables=["instruction"], template=CHINESE_ESSAY_SCORING_TEMPLATE
)

# 视频推荐的prompt
VIDEO_RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=["instruction", "video_info"], template=VIDEO_RECOMMENDATION_TEMPLATE
)

INSPIRATION_PROMPT = PromptTemplate(
    input_variables=["instruction"], template=INSPIRATION_TEMPLATE
)

QA_PROMPT = PromptTemplate(
    input_variables=["text", "query"], template=QA_TEMPLATE
)

# 根据视频总结出题的选择题prompt
VIDEO_QUESTION_CHOICE_PROMPT = PromptTemplate(
    input_variables=["summary", "instruction", "subject"], template=VIDEO_QUESTION_CHOICE_TEMPLATE
)

# 根据视频总结出题的简答题prompt
VIDEO_QUESTION_SHORT_ANSWER_PROMPT = PromptTemplate(
    input_variables=["summary", "instruction", "subject"], template=VIDEO_QUESTION_SHORT_ANSWER_TEMPLATE
)
