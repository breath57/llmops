

class TestLangchainCpt:

    def test_text_splitor(self):
        from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""])
        text = "这是一个测试文本。\n它包含多行内容。\n我们要把它分成多个块。"
        docs = splitter.create_documents([text])
        assert len(docs) > 0

    def test_logger(self):
        pass

    def test_retriever(self):
        from langchain.retrievers import (
            MultiVectorRetriever, 
            BM25Retriever,
            SelfQueryRetriever,
            ContextualCompressionRetriever,
            EnsembleRetriever
            )
        
        from langchain.vectorstores import FAISS
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.storage import InMemoryByteStore
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.prompts import ChatPromptTemplate
        from langchain.chat_models import ChatOpenAI
        from langchain_core.documents import Document


        # 检索器的用法


        # 加载存储库
        from pathlib import Path
        vectorstore = None
        # 加载文档到向量库
        if not Path("faiss_index").exists():
            vectorstore = FAISS.from_documents([
                Document(page_content="Hello, world!")
                ], OpenAIEmbeddings("Qwen/Qwen3-Embedding-4B"))
            # 持久化到本地
            vectorstore.save_local("faiss_index")
        else:
            # 从本地加载
            vectorstore = FAISS.load_local("faiss_index")

        # 创建检索器
        retriever = MultiVectorRetriever(
            vectorstore=vectorstore, 
            byte_store=InMemoryByteStore(), 
            id_key="id")

        # 检索
        retriever.get_relevant_documents("Hello, world!")
        
        
