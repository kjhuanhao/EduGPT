# -*- coding:utf-8 -*-
# @FileName  : app.py.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : APP启动程序

import gradio as gr
import pandas as pd
from service.score_analyzer_service import update_result, execute_score_analyzer
from service.generate_question_service import generate_question
from service.initialize import initialize_state, set_env
from service.brush_questions_service import update_question_info
from service.plugins_service import input_tip, output_chatbot
from service.create_summary_service import create_summary
from service.qa_with_video_service import generate_qa
from service.generate_question_service import remove_question


def get_state_data(state, key):
    return state[key]


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    global_state = initialize_state()
    local_state = gr.State({})
    subject_types = global_state["subject_types"]
    plugins = global_state["plugins"]

    gr.Markdown("# Welcome to EduGPT! 🌟🚀")
    gr.Markdown("为教育降本增效的AI应用")

    with gr.Tab("🔥️主页"):
        gr.Markdown("## ❤️感谢你使用本应用，在开始前请确保下面的配置你都进行了设置，可以点击确定按钮，将为你检测配置状态")
        with gr.Row():
            with gr.Column():
                model = gr.Radio(choices=["openai", "ernie"], label="模型选择", value="openai", interactive=True)
                access_info = gr.Textbox(label="鉴权信息Key or Token")
                bilibili_SESSDATA = gr.Textbox(label="Bilibili SESSDATA(可选)")
                proxy_url = gr.Textbox(label="代理地址(可选)", value="")

            with gr.Column():
                toggle_dark = gr.Checkbox(label="切换主题")
                info = gr.Label(value="❌状态：未设置", show_label=False)
                toggle_dark.select(
                    None,
                    _js="""
                    () => {
                        document.body.classList.toggle('dark');
                    }
                    """,
                )
        gr.Button("确定").click(fn=set_env, inputs=[model, access_info, bilibili_SESSDATA, proxy_url], outputs=info)

        # with gr.Box():
        #     gr.Markdown("- 项目地址: https://github.com/kjhuanhao/EduGPT/tree/dev")
        #     gr.Markdown("- 作者: [LaiJiahao](https://github.com/kjhuanhao)")
        #     gr.Markdown("- 作者: [LinZihao](https://github.com/lindate)")


    """
    【教师】智能成绩分析师
    """
    with gr.Tab("【教师】智能成绩分析师"):
        gr.Markdown("# 【教师】智能成绩分析师 ")
        gr.Markdown("## 上传要分析的成绩单")
        with gr.Row():
            # 文件上传组件
            file = gr.File(label="上传文件", file_types=[".csv"])
            # 展示CSV表格组件
        with gr.Row():
            frame = gr.DataFrame(
                wrap=True,
                label="成绩单展示",
                type="pandas",
                visible=False,
                overflow_row_behaviour="show_ends")
            # frame.change(fn=test, inputs=frame)

            # 文件上传 -> 展示到DataFrame
            file.upload(fn=lambda value: gr.DataFrame.update(value=pd.read_csv(value.name), visible=True),
                        inputs=file,
                        outputs=frame,
                        show_progress=True)

            # 文件取消 -> 清空DataFrame
            file.clear(fn=lambda: gr.DataFrame.update(value=None, visible=False), outputs=frame)

        gr.Markdown("## 分析结果")
        with gr.Row(equal_height=True):
            analyzer_plot = gr.Plot(label="图像分析", show_label=True)
            analyzer_textbox = gr.Textbox(label="数据探索", show_label=True, lines=8, visible=False)

        gr.Markdown("## 分析设置")
        with gr.Row():
            # 展示分析方法组件
            dimension = gr.Radio(
                choices=["图像分析", "数据探索"],
                label="分析方法",
                type="index",
                value="图像分析",
                interactive=True)
            dimension.change(fn=update_result, inputs=dimension, outputs=[analyzer_plot, analyzer_textbox])
            # 文本输入组件
            desc_input = gr.Textbox(placeholder="输入你想获得的数据，例如: 展示所有Test的最高分和最低分",
                                    label="分析目标")

        analyzer_button = gr.Button(value="开始分析", variant="primary")
        analyzer_button.click(fn=execute_score_analyzer,
                              inputs=[desc_input, file, dimension],
                              outputs=[analyzer_plot, analyzer_textbox],
                              )
    """
    网课总结
    """
    with gr.Tab("网课总结"):
        gr.Markdown("# 网课总结")
        with gr.Row(equal_height=True):
            with gr.Column():
                bv_input = gr.Textbox(placeholder="请输入你想要生成总结的视频链接",
                                      label="输入视频链接(当前仅支持Bilibili)",
                                      value='https://www.bilibili.com/video/BV1th411W7PA/?spm_id_from=333.788&vd_source=984365527a4368550ac4049d945cacc3',
                                      interactive=True,
                                      max_lines=4)

                p_input = gr.Textbox(placeholder="请输入分P号，默认为0",
                                     label="输入分P号",
                                     value="0",
                                     interactive=True,
                                     max_lines=4)

                summary_button = gr.Button("开始总结")

                with gr.Box():
                    with gr.Box():
                        gr.Markdown("# Q&A bot")
                        chatbot = gr.Chatbot(label="AI Answer")
                        qa_input = gr.Textbox(label="Chat With Video", interactive=True,
                                              placeholder="在这里输入你的问题")
                        with gr.Row():
                            clear = gr.ClearButton([qa_input, chatbot], value="清除")
                            send_button = gr.Button(value="发送")

            with gr.Column():
                info_output = gr.Textbox(
                    interactive=False,
                    lines=27,
                    label="视频字幕",
                    show_label=True, )

                summary_output = gr.Textbox(
                    interactive=False,
                    lines=10,
                    label="AI总结",
                    show_label=True, )


                summary_button.click(fn=create_summary,
                                     inputs=[bv_input, p_input],
                                     outputs=[info_output, summary_output])

                send_button.click(fn=generate_qa, inputs=[info_output, qa_input, chatbot], outputs=[qa_input, chatbot])

    """
    题目生成
    """
    # 选择后去获取本地课程
    with gr.Tab("题目生成"):
        gr.Markdown("# 智能题目生成助手")
        with gr.Box():
            with gr.Row():
                show_question = gr.Textbox(
                    interactive=False,
                    lines=5,
                    label="题目生成结果(题目生成后会自动保存到本地题库中)",
                    show_label=True)

            with gr.Row():
                with gr.Column():
                    # summary出题
                    question_type = gr.Radio(
                        choices=["选择题", "简答题"],
                        type="value",
                        value="选择题",
                        interactive=True,
                        label="题目类型",
                        show_label=True)

                    subject_type = gr.Radio(
                        choices=subject_types,
                        type="value",
                        value="History",
                        interactive=True,
                        label="科目类型",
                        show_label=True)

                    # course = gr.Dropdown(choices=local_state.value["course_title_list"], label="根据看过的课程出题(可为空)", show_label=True)
                    # refresh_button = gr.Button(value="刷新课程列表")
                    # refresh_button.click(fn=get_course_list, inputs=local_state, outputs=local_state)
                    # course.select(fn=select_course, inputs=[course, local_state], outputs=local_state)

                with gr.Column():
                    desc_input = gr.Textbox(placeholder="请描述你想要生成的题目，例如：有关中国外交的近代史",
                                            label="题目描述")

                    generate_button = gr.Button(value="生成题目", variant="primary")

                    remove_button = gr.ClearButton(value="移除题目", variant="stop")

                    remove_button.click(fn=remove_question, inputs=[show_question, subject_type], outputs=show_question)

                    generate_button.click(fn=generate_question,
                                          inputs=[question_type, desc_input, subject_type],
                                          outputs=show_question)

    """
    【学生】刷题工具
    """
    with gr.Tab("【学生】刷题工具"):
        gr.Markdown("# 【学生】刷题工具 ")
        with gr.Row():
            gr.Markdown("## 题库")
            # 题库科目选择组件
        with gr.Row():
            select_subject_types = gr.Radio(
                choices=subject_types,
                label="科目类型",
                show_label=True,
                type="value")

        with gr.Row():
            with gr.Column():
                # gr.Markdown("## 题目")

                show_question = gr.Label(value="选择一个科目类型开始刷题吧！", label="题目", show_label=True)
                # verify_answer = gr.Button(value="检查")

                # 选择题组件
                answer_choices = gr.Radio(
                    choices=[],
                    min_width=10,
                    interactive=True,
                    label="选择题",
                    show_label=True,
                    visible=False)
                # 填空题组件
                answer_short = gr.Textbox(
                    placeholder="请输入你的答案",
                    visible=False,
                    label="填空题",
                    interactive=True,
                    show_label=True
                )
                # 题库科目选择 -> 题目选择
                select_subject_types.change(
                    fn=update_question_info,
                    inputs=[local_state, select_subject_types],
                    outputs=[answer_choices, answer_short, show_question, local_state]
                )

            # 点击下一题的时候需要判断是否选择了答案
            with gr.Column():
                show_text = gr.Textbox(lines=15, show_label=False, interactive=False)
                get_clue = gr.Button(value="获取提示")
                get_answer = gr.Button(value="获取答案")
                get_question = gr.Button(value="下一题")

                get_clue.click(fn=lambda state: state["clue"], inputs=[local_state], outputs=show_text)
                get_answer.click(fn=lambda state: state["answer_explanation"], inputs=[local_state], outputs=show_text)

                get_question.click(
                    fn=update_question_info,
                    inputs=[local_state, select_subject_types],
                    outputs=[answer_choices, answer_short, show_question, local_state],
                    show_progress=True)

                # 监听label是否改变
                show_question.change(fn=lambda: gr.update(value=None), outputs=show_text)

    """
    插件
    """
    with gr.Tab("智能AI插件"):
        gr.Markdown("# 智能AI插件")
        chatbot = gr.Chatbot()
        with gr.Row():
            plugins_select = gr.Dropdown(choices=plugins, interactive=True, label="插件选择", show_label=True)
            tip = gr.Label(label="输入提示", value="请选择一个插件", show_label=True)
            plugins_select.change(fn=input_tip, inputs=plugins_select, outputs=tip)
        input_instruction = gr.Textbox(label="输入指令", show_label=True, placeholder="请根据提示输入指令", lines=9)
        with gr.Row():
            run_button = gr.Button(value="Run", variant="primary")
            run_button.click(fn=output_chatbot, inputs=[plugins_select, input_instruction, chatbot],
                             outputs=[input_instruction, chatbot])
            clear_button = gr.ClearButton([input_instruction, chatbot])

if __name__ == "__main__":
    demo.launch()
