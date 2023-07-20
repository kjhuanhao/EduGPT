# -*- coding:utf-8 -*-
# @File      : create_summary.py
# @Time      : 2023/7/20
# @Author    : LinZiHao
# @Desc      : 总结业务模块
import os

import gradio as gr
from utils.bili_subtitle_downloader import BiliSubtitleDownloader
from utils.summary_writer import SummaryWriter


def create_summary(bv_input: str, p_input: int, cookie_input: str):
    """
    生成总结
    :param bv_input: 视频bv号
    :param p_input: 分集号
    :param cookie_input: cookie
    """

    # 下载字幕
    bili_subtitle_downloader = BiliSubtitleDownloader(bv_input, int(p_input), cookie_input)
    bili_info = bili_subtitle_downloader.get_bili_info()

    bili_subtitle = bili_info["subtitle"]

    # 生成总结
    summary_writer = SummaryWriter(bili_info).write_summary()

    return [gr.update(value=bili_subtitle), gr.update(value=summary_writer)]


# create_summary(bv_input='BV1ps4y1m75J', p_input=0, cookie_input=os.getenv("BILIBILI_COOKIE"))









