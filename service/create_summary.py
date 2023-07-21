# -*- coding:utf-8 -*-
# @File      : create_summary.py
# @Time      : 2023/7/20
# @Author    : LinZiHao
# @Desc      : 总结业务模块
import os

import gradio as gr
from utils.bili_subtitle_downloader import BiliSubtitleDownloader
from utils.summary_writer import SummaryWriter
from utils.cache_handler import CacheHandler


def create_summary(bv_input: str, p_input: str):
    """
    生成总结
    :param bv_input: 视频bv号
    :param p_input: 分集号
    """
    # 下载字幕
    bili_info = BiliSubtitleDownloader(bv_input, p_input).get_bili_info()
    bili_subtitle = BiliSubtitleDownloader(bv_input, p_input)._download_subtitle()
    print(bili_subtitle)
    print(bili_info["cid"])

    bili_b_cid = bili_info["bv_id"] + str(bili_info["cid"])
    print(bili_b_cid)

    if CacheHandler().judge_subtitle_cache(bili_b_cid) is None:
        bili_info["subtitle"] = bili_subtitle
        bili_summary = SummaryWriter(bili_info).write_summary()
        return [gr.update(value=bili_subtitle), gr.update(value=bili_summary)]
    else:
        bili_info_cache = CacheHandler().judge_subtitle_cache(bili_b_cid)
        bili_subtitle = bili_info_cache["subtitle"]
        bili_summary = bili_info_cache["summary"]
        return [gr.update(value=bili_subtitle), gr.update(value=bili_summary)]


if __name__ == '__main__':
    create_summary(bv_input='BV1ps4y1m75J', p_input="0")

