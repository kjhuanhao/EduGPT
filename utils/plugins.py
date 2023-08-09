# -*- coding:utf-8 -*-
# @FileName  : plugins.py
# @Time      : 2023/7/19
# @Author    : LaiJiahao
# @Desc      : 学习计划指定

from common.config import Config
from prompt.structured_prompt import (
    STUDY_PLAN_PROMPT,
    CHINESE_ESSAY_SCORING_PROMPT,
    VIDEO_RECOMMENDATION_PROMPT,
    INSPIRATION_PROMPT
)
from loguru import logger
from bilibili_api import sync
from bilibili_api import search
from typing import List


class Plugins:
    """
    多插件

    """

    def __init__(self, instruction: str):
        self.instruction = instruction
        self._llm = Config().get_llm()

    def generate_study_plan(self):
        """
        生成学习计划
            Example:
            我在(两)周内。可以每周的(周一周二)每天学习(2)小时 ,我的学习主题是: (中国古代史) , 所属的科目是: (历史)
        """
        logger.info("正在生成学习计划")
        _llm_chain = Config.create_llm_chain(llm=self._llm, prompt=STUDY_PLAN_PROMPT)
        response = _llm_chain.run(
            instruction=self.instruction
        )
        logger.info("学习计划制作完毕")
        return response

    def score_chinese_essay(self):
        """
        生成语文作文评分
            Example:
            请给我评分，我的作文题目是: (xx)，我的作文内容是: (xx)
        """
        logger.info("正在进行语文作文评分")
        llm_chain = Config.create_llm_chain(llm=self._llm, prompt=CHINESE_ESSAY_SCORING_PROMPT)
        response = llm_chain.run(
            instruction=self.instruction
        )
        logger.info("语文作文评分完毕")
        return response

    def recommend_course(self):
        """
        推荐课程
            Example:
                (学习主题)
        """
        logger.info("正在查询相关的视频信息")
        v_response = sync(search.search_by_type(keyword=self.instruction, search_type=search.SearchObjectType.VIDEO))
        result = []
        for video_info in v_response["result"]:
            video_infos = {"title": video_info["title"],
                           "description": video_info["description"],
                           "acurl": video_info["arcurl"]}
            result.append(video_infos)

        logger.info("AI智能推荐中")
        llm_chain = Config.create_llm_chain(llm=self._llm, prompt=VIDEO_RECOMMENDATION_PROMPT)
        response = llm_chain.run(
            instruction=self.instruction,
            video_info=str(result)
        )
        logger.info("AI智能推荐完毕")
        return response

    def get_inspiration(self, chat_history: List):
        """
        启发式学习
            Example:
                (对话)
        """
        conversation_chain = Config.create_llm_chain(llm=self._llm, prompt=INSPIRATION_PROMPT)
        # 如果List有信息，会是[[user,ai]]
        message = "\n"
        if len(chat_history) > 0:
            k = 0  # 对话的轮次
            for dialogue in chat_history:
                if k > 5:
                    break
                message += f"User: {dialogue[0]}\nAI: {dialogue[1]}\n"
                k += 1
        message += f"User:{self.instruction}\nAI: "
        logger.info(message)
        response = conversation_chain.run(
            instruction=message
        )
        return response
