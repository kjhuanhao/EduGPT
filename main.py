# -*- coding:utf-8 -*-
# @FileName  : main.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : None

from utils.score_analyzer import ScoreAnalyzer
import pandas as pd


# df = pd.read_csv("./resources/student_marks.csv")
# a = ScoreAnalyzer(df)
# a.plot_df("展示所有Test的最高分和最低分")
# a.plot_df("展示所有Test的最高分和最低分")
# text = "\nimport plotly.express as px\n\n# Create a histogram plot for Test_1 scores\nfig = px.histogram(df, x='Test_1')\n\n# Set the title and axis labels\nfig.update_layout(\n    title_text='Distribution of Test_1 Scores',\n    xaxis_title='Test_1 Score',\n    yaxis_title='Count'\n)\n\n# Display the plot\nfig.show()\n"
# exec(text)

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

test_summary()