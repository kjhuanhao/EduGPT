# -*- coding:utf-8 -*-
# @FileName  : toolkit.py
# @Time      : 2023/7/19
# @Author    : LaiJiahao
# @Desc      : Edu工具箱

from enum import Enum


class Toolkit(Enum):
    """
    Edu工具箱，当前包括
    1. 学习计划制定
    2. 作文评分
    """
    StudyPlanDevelopment = "学习计划制定"
    ChineseEssayScoring = "语文作文评分"
    VideoRecommendation = "学习视频推荐"
    Inspiration = "启发式学习"
