# -*- coding:utf-8 -*-
# @File      : qa_generator.py
# @Time      : 2023/7/17
# @Author    : LinZiHao
# @Desc      : 文本 Q&A

import os

from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.base_language import BaseLanguageModel
from typing import List, Optional
from loguru import logger

load_dotenv(find_dotenv(), override=True)

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)


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
                 llm: Optional[BaseLanguageModel] = None,

                 ) -> None:
        """
        :param qa_text: 要进行Q&A的文本
        :param query: 提问词
        :param llm: 自定义llm，默认gpt-3.5-turbo
        """
        self.qa_text = qa_text
        self.seg_length = 3400
        self.query = query
        if llm is None:
            llm = ChatOpenAI(model_name=os.getenv("CHAT_MODEL"),
                             temperature=0,
                             )
        self._llm = llm

    def _text_splitter(self) -> List[str]:
        logger.info("执行文本分割")
        # 创建拆分器
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.seg_length, chunk_overlap=200)
        # 拆分文本
        qa_split_text = text_splitter.split_text(self.qa_text)
        return qa_split_text

    def qa_generator(self):
        logger.info("正在生成回复")
        # 创建embeddings
        embeddings = OpenAIEmbeddings()
        # 创建向量存储，使得我们可以进行相关性搜索
        textsearch = FAISS.from_texts(self._text_splitter(), embeddings)
        qa = RetrievalQA.from_chain_type(llm=self._llm, chain_type="stuff", retriever=textsearch.as_retriever())
        result = qa.run(self.query)
        return result


