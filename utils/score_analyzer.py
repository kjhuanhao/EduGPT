# -*- coding:utf-8 -*-
# @FileName  : score_analyzer.py
# @Time      : 2023/7/15
# @Author    : LaiJiahao
# @Desc      : None

import os
import re
import pandas as pd

from common.config import Config
from loguru import logger
from pandas import DataFrame
from typing import Dict
from prompt.structured_prompt import PLOT_PROMPT
from pandasai import PandasAI
from exceptions.plot_exception import PlotException


class ScoreAnalyzer:
    """
    分数分析器
    Example:
        score_analyzer = ScoreAnalyzer(df)
        # 生成图表
        score_analyzer.plot_df("your_desc")
        # 与数据交互
        score_analyzer.chat_with_data("your_desc")
    """

    def __init__(
            self,
            file_path: str
    ) -> None:
        if not os.path.exists(file_path):
            raise Exception("该文件不存在")
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self._schema_str = self._get_df_schema(self.df)
        self._llm = Config().get_llm()
        self._plot_chain = Config.create_llm_chain(self._llm, PLOT_PROMPT)

    def plot_df(
            self,
            desc: str
    ) -> Dict:
        """
        生成图表
        :param desc: 对图标的指令描述
        :return: None
        """
        instruction = f"The purpose of the plot: {desc}"

        logger.info("正在执行Plot Chain AI")
        response = self._plot_chain.run(
            columns=self._schema_str,
            example=self.df.head(1).to_string(),
            file_path=self.file_path,
            instruction=instruction
        )
        codeblocks = self._get_code_blocks(response)
        result = {
            "codeblocks": codeblocks,
            "response": response
        }
        # self._cache.output_cache(output)
        # print(response)

        logger.info("成功返回Plot Chain AI结果")

        return result

    def chat_with_data(self, desc) -> str:
        """
        对CSV数据进行交互
        :param desc: 询问描述
        :return: 询问结果
        """
        logger.info("正在运行Pandas AI")
        desc += " 请使用中文回复"
        pandas_ai = PandasAI(self._llm, conversational=False)
        response = pandas_ai.run(self.df, desc)

        logger.info("成功返回Pandas AI结果")
        return response

    @staticmethod
    def _get_df_schema(df: DataFrame) -> str:
        """
        获得dataFrame中的头部信息
        :param df: dataframe数据
        :return: 头部信息
        """
        return "\n".join([f"{name}: {dtype}" for name, dtype in df.dtypes.items()])

    @staticmethod
    def _get_code_blocks(markdown: str) -> str:
        """
        获得Markdown文本中的代码块部分
        :param markdown: LLM生成的结果
        :return: Python代码
        """
        pattern = r"```python(.*?)```"
        code_blocks = re.findall(pattern, markdown, re.DOTALL)
        if len(code_blocks) == 0:
            raise PlotException("没有找到可执行的python代码块")
        else:
            return "\n".join(code_blocks)
