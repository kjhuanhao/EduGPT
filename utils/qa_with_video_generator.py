# -*- coding:utf-8 -*-
# @File      : qa_with_video_generator.py
# @Time      : 2023/7/17
# @Author    : LinZiHao
# @Desc      : 文本 Q&A

from common.config import Config
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from prompt.structured_prompt import QA_PROMPT
from typing import List
from loguru import logger


class QAGenerator:
    """
        文本 Q&A
    Example:
        qa_generator = QAGenerator(subtitle, query=)
        result = qa_generator.qa_generator()
    """

    def __init__(self,
                 qa_text: str,
                 query: str,
                 ) -> None:
        """
        :param qa_text: 要进行Q&A的文本
        :param query: 提问词
        """
        self.qa_text = qa_text
        self.seg_length = 3000
        self.query = query
        self._llm = Config().get_llm()
        self._chain = Config.create_llm_chain(self._llm, QA_PROMPT)

    def _text_splitter(self) -> List[str]:
        logger.info("执行文本分割")
        # 创建拆分器
        text_splitter = CharacterTextSplitter(chunk_size=self.seg_length, chunk_overlap=200)
        # 拆分文本
        qa_split_text = text_splitter.split_text(self.qa_text)
        return qa_split_text

    def qa_generator(self):
        logger.info("正在生成回复")
        # 创建embeddings
        embeddings = OpenAIEmbeddings()
        # 创建向量存储，使得我们可以进行相关性搜索
        textsearch = FAISS.from_texts(self._text_splitter(), embeddings)
        similarity_texts_lists = textsearch.similarity_search(self.query, k=4)
        similarity_texts = ""

        for text in similarity_texts_lists:
            similarity_texts += f"{text.page_content} \n"
        result = self._chain.run(
            text=similarity_texts,
            query=self.query
        )
        logger.info("正在返回回复")
        return result
