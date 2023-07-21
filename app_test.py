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
            with gr.Column():
                bv_input = gr.Textbox(placeholder="请输入你想要生成总结的视频BV号",
                                      label="输入BV号",
                                      interactive=True,
                                      max_lines=4)

                p_input = gr.Textbox(placeholder="请输入分P号，默认为0",
                                     label="输入分P号",
                                     interactive=True,
                                     max_lines=4)
                summary_button = gr.Button("总结")
                with gr.Box():
                    with gr.Box():
                        gr.Markdown("# Q&A bot")
                        chatbot = gr.Chatbot(label="AI Answer")
                        qa_input = gr.Textbox(label="question", interactive=True, placeholder="回车键发送")
                        with gr.Row():
                            clear = gr.ClearButton([qa_input, chatbot])

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
                qa_input.submit(generate_qa, [info_output, qa_input, chatbot], [qa_input, chatbot])

if __name__ == "__main__":
    demo.launch()
