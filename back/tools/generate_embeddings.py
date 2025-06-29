# generate_embeddings.py
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma


def generate_embeddings():
    # 配置参数
    document_path = "../Local/knowledge/med_data.docx"  # 源文档路径
    persist_directory = "Local/embeddings/med_chroma_db"  # 向量库存储路径
    embedding_model = "quentinz/bge-large-zh-v1.5:latest"  # 嵌入模型

    # 加载文档
    loader = Docx2txtLoader(file_path=document_path)
    docs = loader.load()

    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    # 创建并保存向量库
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OllamaEmbeddings(model=embedding_model),
        persist_directory=persist_directory
    )

    print(f"向量库已生成并保存到 {persist_directory}")


if __name__ == "__main__":
    generate_embeddings()
