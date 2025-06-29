import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
from pydantic import PrivateAttr  # 新增导入


# 修正后的自定义Embedding类
class BGEEmbeddings(HuggingFaceEmbeddings):
    # 使用PrivateAttr声明自定义参数
    _query_instruction: str = PrivateAttr()

    def __init__(self, query_instruction: str = "", **kwargs):
        super().__init__(**kwargs)
        self._query_instruction = query_instruction  # 使用私有属性

    def embed_query(self, text: str) -> List[float]:
        if self._query_instruction:
            text = self._query_instruction + text
        return super().embed_query(text)


# 初始化LLM（保持DeepSeek配置不变）
llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key='sk-9eeddedcf63e4ed39a56b59d78b85607',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

# 正确初始化BGE嵌入模型
embedding_model = BGEEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True},
    query_instruction="为这个句子生成表示以用于检索相关文章："  # 现在这个参数会被正确接收
)

# 剩余代码保持不变...
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embedding_model
)

retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

print(rag_chain.invoke("你好，你现在连接了什么RAG知识库？"))
