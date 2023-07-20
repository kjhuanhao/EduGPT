# -*- coding:utf-8 -*-
# @File      : create_summary.py
# @Time      : 2023/7/20
# @Author    : LinZiHao
# @Desc      : Q&A bot模块
import gradio as gr
from utils.qa_generator import QAGenerator


def generate_qa(qa_text: str, query: str):
    """
    生成总结
    :param qa_text: 要进行Q&A的文本
    :param query: 提问词
    """
    result = QAGenerator(qa_text, query=query).qa_generator()
    return gr.update(value=result)

