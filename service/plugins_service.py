# -*- coding:utf-8 -*-
# @FileName  : plugins_service.py
# @Time      : 2023/7/19
# @Author    : LaiJiahao
# @Desc      : AI插件业务模块

import gradio as gr
from entity.toolkit import Toolkit
from utils.plugins import Plugins


def input_tip(plugin_name: str):
    """
    输入提示
    :param plugin_name: 插件名称
    """
    plugins = [value.value for value in list(Toolkit)]
    if plugin_name not in plugins:
        raise gr.Error("当前插件不存在，请重新输入")

    if plugin_name == Toolkit.StudyPlanDevelopment.value:
        return gr.update(
            value="我在(两)周内，可以每周的(周一周二)每天学习(2)小时，我的学习主题是: (中国古代史) ，所属的科目是: (历史)")
    if plugin_name == Toolkit.ChineseEssayScoring.value:
        return gr.update(
            value="请给我评分，我的作文题目是: (xx)，我的作文内容是: (xx)")
    if plugin_name == Toolkit.VideoRecommendation.value:
        return gr.update(
            value="请输入你想要学习的主题，例如: 中国古代史")
    if plugin_name == Toolkit.Inspiration.value:
        return gr.update(
            value="请直接输入你的问题，AI会为你剖析")


def output_chatbot(plugins_select, instruction, chat_history):
    """
    输出聊天机器人
    :param plugins_select: 插件选择
    :param instruction: 指令
    :param chat_history: 聊天记录

    :return: 聊天记录
    """

    plugins = Plugins(instruction)
    bot_message = "请重试！"

    if plugins_select == Toolkit.StudyPlanDevelopment.value:
        bot_message = plugins.generate_study_plan()
    if plugins_select == Toolkit.ChineseEssayScoring.value:
        bot_message = plugins.score_chinese_essay()
    if plugins_select == Toolkit.VideoRecommendation.value:
        bot_message = plugins.recommend_course()
    if plugins_select == Toolkit.Inspiration.value:
        bot_message = plugins.get_inspiration(chat_history)

    chat_history.append((instruction, bot_message))
    return "", chat_history
