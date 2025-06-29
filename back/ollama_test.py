from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_ollama import ChatOllama, OllamaEmbeddings  # 修正导入
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import Docx2txtLoader  # 修改这里
import bs4
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import hub

model = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key="sk-9eeddedcf63e4ed39a56b59d78b85607",
    openai_api_base="https://api.deepseek.com",
    max_tokens=2024
)

# 初始化模型
llm = ChatOllama(
    model="qwen3:8b",
    # model="deepseek-r1",
    # model="deepseek-r1:1.5b",
    # model="qwen3:0.6b",
    temperature=0,
)

persist_directory = "Local/embeddings/med_chroma_db"
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=OllamaEmbeddings(model="quentinz/bge-large-zh-v1.5:latest")
)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

system_template = (
    "你是一位温柔的医生，你需要根据患者的描述判断疾病，并给出建议。"
    "在第一次的回答的第一行直接说明可能的疾病，然后换行，开始进行专业医学回复。"
    "专业医学回复要采用一定格式，首先说出疾病的成因，然后说出症状，然后给出建议，最后建议该挂哪个科室"
    "尝试继续与患者沟通，获得更多信息，更好的分析病情，之后的回复不必拘泥于第一次的格式"
    "适当参考{context}"

)
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    MessagesPlaceholder(variable_name="chat_history"),
    ('user', '{input}')
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# test_chain = RunnableLambda(lambda x: x) | retriever | format_docs
# print(test_chain.invoke("头痛"))


# 测试调用（带历史记录）


chain1 = create_stuff_documents_chain(model, prompt_template)  # 检索
rag_chain = create_retrieval_chain(retriever, chain1)
# res = rag_chain.invoke({"input": "头痛", "chat_history": []})
# print(res)
chain = rag_chain.pick("answer")
for chunk in chain.stream({"input": "头痛", "chat_history": []}):
    print(f"{chunk}", end="")
