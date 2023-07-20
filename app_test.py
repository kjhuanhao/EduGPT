# -*- coding:utf-8 -*-
# @File      : app_test.py
# @Time      : 2023/7/18
# @Author    : LinZiHao
# @Desc      : None

import gradio as gr
from service.create_summary import create_summary
from service.qa_service import generate_qa


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    """
    视频文本智能总结
    """
    with gr.Tab("视频文本智能总结"):
        gr.Markdown("# 智能总结助手")
        with gr.Row(equal_height=True):
            with gr.Row(equal_height=True):
                bv_input = gr.Textbox(placeholder="请输入你想要生成总结的视频BV号",
                                      label="输入BV号",
                                      interactive=True,
                                      max_lines=4)

                p_input = gr.Textbox(placeholder="若视频为合集，请输入分集号，默认为0",
                                     label="输入分集号",
                                     interactive=True,
                                     max_lines=4)

                cookie_input = gr.Textbox(placeholder="请输入你的cookie",
                                          label="输入cookie",
                                          interactive=True,
                                          max_lines=4)

                with gr.Column():
                    summary_button = gr.Button("总结")
                    with gr.Box():
                        gr.Markdown("## Q&A bot")
                        qa_output = gr.TextArea(label="AI Answer",
                                                interactive=False)
                        qa_input = gr.Textbox(placeholder="想问的问题问这~~",
                                              label="Question",
                                              interactive=True)
                        with gr.Row(equal_height=True):
                            clear = gr.ClearButton([qa_input, qa_output])
                            qa_button = gr.Button("发送")

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
                                     inputs=[bv_input, p_input, cookie_input],
                                     outputs=[info_output, summary_output])
                qa_button.click(fn=generate_qa,
                                inputs=[info_output, qa_input],
                                outputs=qa_output)

if __name__ == "__main__":
    demo.launch()
