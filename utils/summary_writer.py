import os

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional
from prompt.structured_prompt import SUMMARY_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts import BasePromptTemplate
from loguru import logger

load_dotenv(find_dotenv(), override=True)


class SummaryWriter:
    """
    文本总结
    Example:

        summary_writer = SummaryWriter(text)
        # 生成摘要
        summary = summary_writer.write_summary()
        # 输出摘要内容
        print(summary)
    """

    def __init__(self,
                 text: str,
                 summary_count: Optional[int] = None,
                 llm: Optional[BaseLanguageModel] = None,
                 ) -> None:
        """
        :param text:要进行摘要生成的文本
        :param summary_count:生成摘要的条目数量（默认为 10）
        """
        self.text = text
        self.seg_length = 3400
        self.summary_count = 10 if summary_count is None else summary_count
        self._handler = StreamingStdOutCallbackHandler()
        if llm is None:
            llm = ChatOpenAI(model_name=os.getenv("CHAT_MODEL"),
                             temperature=0,
                             callbacks=[self._handler],
                             streaming=True
                             )
        self._llm = llm
        self._summary_chain = self._create_llm_chain(prompt=SUMMARY_PROMPT)

    def write_summary(self) -> str:
        """
        拼接返回的总结文本
        :return: 总结文本
        """
        ans = ""
        for chunk in self._seg_content():
            ans += self._get_summary(chunk)
        logger.info("完成总结")
        return ans

    def _seg_content(self) -> List[str]:
        """
        将文本按照指定的段落长度(seg_length = 3400)划分成多个段落
        :return: 划分后的段落列表
        """
        logger.info("执行分割文本")
        r_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.seg_length,
            chunk_overlap=200
        )
        split_texts = r_splitter.split_text(self.text)
        return split_texts

    def _get_summary(self, chunk) -> str:
        logger.info("执行总结任务")
        response = self._summary_chain.run(
            summary_count=self.summary_count,
            subtitle=chunk
        )
        return response

    def _create_llm_chain(self, prompt: BasePromptTemplate):

        return LLMChain(llm=self._llm, prompt=prompt)

