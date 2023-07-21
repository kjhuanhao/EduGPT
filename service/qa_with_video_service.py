# -*- coding:utf-8 -*-
# @File      : create_summary_service.py
# @Time      : 2023/7/20
# @Author    : LinZiHao
# @Desc      : Q&A bot模块
from utils.qa_with_video_generator import QAGenerator


def generate_qa(qa_text: str, query: str, chat_history):
    """
    生成总结
    :param qa_text: 要进行Q&A的文本
    :param query: 提问词
    :param chat_history: chat_history
    """
    bot_message = QAGenerator(qa_text, query=query).qa_generator()
    chat_history.append((query, bot_message))
    return "", chat_history
