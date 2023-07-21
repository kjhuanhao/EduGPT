# -*- coding:utf-8 -*-
# @FileName  : score_analyzer_service.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : 数据分析业务模块

from utils.score_analyzer import ScoreAnalyzer
import gradio as gr


def update_result(choice):
    """
    更新图像和文字组件
    :param choice: 0: 展示图像，1: 展示文字
    :return: 更新结果
    """
    if choice == 0:
        return [gr.update(visible=True), gr.update(visible=False)]
    if choice == 1:
        return [gr.update(visible=False), gr.update(visible=True)]


def execute_score_analyzer(desc: str, file_, choice: int):
    """
    执行成绩分析
    :param desc: 分析目标
    :param file_: 文件
    :param choice: 0: 展示图像，1: 展示文字
    """
    if desc is None:
        raise gr.Error("请输入分析目标")
    if file_ is None:
        raise gr.Error("请上传文件")

    try:
        file_name = str(file_.name).replace("\\", "/")
        score_analyzer = ScoreAnalyzer(file_name)
        if choice == 0:
            result = score_analyzer.plot_df(desc)
            codeblocks = result["codeblocks"]
            exec(codeblocks, globals(), locals())
            func = eval('chart_plot()', globals(), locals())
            return [gr.update(value=func), gr.update()]

        if choice == 1:
            result = score_analyzer.chat_with_data(desc)
            return [gr.update(), gr.update(value=result)]
    except Exception as e:
        raise gr.Error("分析失败，请重试")
