# -*- coding:utf-8 -*-
# @FileName  : app.py.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : None

import gradio as gr
import pandas as pd
from service.score_analyzer_service import update_result, execute_score_analyzer
from service.generate_question_service import generate_question
from service.initialize import initialize_state
from service.brush_questions import update_question_info


def get_state_data(state, key):
    return state[key]


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    global_state = initialize_state()
    local_state = gr.State({})
    subject_types = global_state["subject_types"]
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

        analyzer_button = gr.Button(value="开始分析")
        analyzer_button.click(fn=execute_score_analyzer,
                              inputs=[desc_input, file, dimension],
                              outputs=[analyzer_plot, analyzer_textbox],
                              )
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
    【学生】题目生成
    """
    with gr.Tab("【学生】题目生成"):
        gr.Markdown("# 智能题目生成助手")
        with gr.Box():
            with gr.Row():
                show_result = gr.Textbox(
                    interactive=False,
                    lines=5,
                    label="题目生成结果(题目生成后会自动保存到本地题库中，点击移除按钮可以移除)",
                    show_label=True)

            with gr.Row():
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
            with gr.Row():
                with gr.Column():
                    desc_input = gr.Textbox(placeholder="请描述你想要生成的题目，例如：有关中国外交的近代史",
                                            label="题目描述")
                with gr.Column():
                    generate_button = gr.Button(value="生成题目")
                    remove_button = gr.ClearButton(value="移除题目", variant="stop")
                    generate_button.click(fn=generate_question, inputs=[question_type, desc_input, subject_type],
                                          outputs=show_result)

if __name__ == "__main__":
    demo.launch()
