# -*- coding:utf-8 -*-
# @FileName  : app.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : None

from utils.score_analyzer import ScoreAnalyzer
from utils.question_assistant import QuestionAssistant
from entity.subject import SubjectType


def test_analyzer():
    a = ScoreAnalyzer("./resources/student_marks.csv")
    a.plot_df("展示所有Test的最高分和最低分")
    # a.chat_with_data("Test1到Test12中，所有学生的总成绩最高的学生ID")


# test_analyzer()


def test_summary():
    from utils.bili_subtitle_downloader import BiliSubtitleDownloader
    from utils.summary_writer import SummaryWriter
    bv_id = 'BV1ps4y1m75J'  # 替换为视频的 BV 号
    p_num = 0  # 替换为视频的分集号，从 0 开始

    downloader = BiliSubtitleDownloader(bv_id, p_num)
    subtitle = downloader.download_subtitle()
    print(f'CC 字幕内容: {subtitle}')

    summary_writer = SummaryWriter(subtitle)
    # 生成摘要
    summary = summary_writer.write_summary()
    # 输出摘要内容
    print(summary)


def test_question_assistant():
    question_assistant = QuestionAssistant()
    question_assistant.generate_choice_question(desc="关于中国古代农业生产力", subject=SubjectType.History)
    # question_assistant.generate_short_answer_question(desc="关于中国古代农业生产力", subject=SubjectType.History)


# test_question_assistant()

def test_init():
    from service.initialize import initialize_state
    initialize_state()


def test_plugins():
    from utils.plugins import Plugins
    plugins = Plugins("中国古代史")
    print(plugins.recommend_course())


test_plugins()
