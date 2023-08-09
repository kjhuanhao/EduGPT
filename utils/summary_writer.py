# -*- coding:utf-8 -*-
# @FileName  : summary_writer.py
# @Time      : 2023/7/17
# @Author    : LinZihao
# @Desc      : 总结文本
from common.config import Config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional
from prompt.structured_prompt import SUMMARY_PROMPT
from utils.cache_handler import CacheHandler
from loguru import logger


class SummaryWriter:
    """
    文本总结
    Example:
        summary_writer = SummaryWriter(text)
        # 生成摘要
        summary = summary_writer.write_summary()
    """

    def __init__(self,
                 summary_info: dict,
                 summary_count: Optional[int] = None
                 ) -> None:
        """
        :param summary_info:要进行摘要生成的文本
        :param summary_count:生成摘要的条目数量（默认为 10）
        """
        self.b_cid = summary_info["bv_id"] + str(summary_info["cid"])
        self.title = summary_info["title"]
        self.subtitle = summary_info["subtitle"]
        self.seg_length = 3000
        self.summary_count = 5 if summary_count is None else summary_count
        self._llm = Config().get_llm()
        self._summary_chain = Config.create_llm_chain(llm=self._llm, prompt=SUMMARY_PROMPT)
        self._cache_handler = CacheHandler()

    def write_summary(self) -> str:
        """
        拼接返回的总结文本
        :return: 总结文本
        """
        summary_ans = ""
        pre_summary_text = self._summary_seg_content()
        for chunk in pre_summary_text:
            summary_ans += self._get_summary(chunk)
        if len(pre_summary_text) >= 2:
            summary_ans = self._get_summary(summary_ans)

        self._cache_handler.subtitle_cache(b_cid=self.b_cid,
                                           title=self.title,
                                           subtitle=self.subtitle,
                                           summary=summary_ans)
        logger.info("返回总结")
        return summary_ans

    def _summary_seg_content(self) -> List[str]:
        """
        将文本按照指定的段落长度(seg_length = 3400)划分成多个段落
        :return: 划分后的段落列表
        """
        if len(self.subtitle) > self.seg_length:
            logger.info("执行文本分割")
            r_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.seg_length,
                chunk_overlap=200
            )
            split_texts = r_splitter.split_text(self.subtitle)
            return split_texts
        else:
            return [self.subtitle]

    def _get_summary(self, chunk) -> str:
        logger.info("执行总结任务")
        summary_response = self._summary_chain.run(
            summary_count=self.summary_count,
            subtitle=chunk
        )
        return summary_response
