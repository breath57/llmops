import pytest
from dotenv import load_dotenv
load_dotenv()


class TestRetriever:
    def test_bm25_retriever(self):
        from langchain_community.retrievers import BM25Retriever
        from langchain_core.documents import Document

        # 1. 准备文档
        docs = [
            Document(page_content="Python 是一种编程语言，适合数据分析"),
            Document(page_content="Java 是一种强类型语言，适合企业级开发"),
            Document(page_content="小雨喜欢吃\"编程\"饼干"),
            Document(page_content="编制喜欢的程序啊？"),
        ]

        # 2. 初始化 BM25Retriever
        retriever = BM25Retriever.from_documents(docs)
        retriever.k = 2  # 检索 top 2

        # 3. 检索（对关键词“编程语言”敏感）
        docs = retriever.invoke("编程语言有哪些？")

        print(docs)