# main.py

from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

import os

# === CONFIGURATION ===
PDF_PATH = "data/BonBon FAQ.pdf"
DB_PATH = "./db"
COLLECTION_NAME = "text_collection"


def load_or_create_chroma_db():
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(DB_PATH):
        print("📂 Loading existing vector DB...")
        return Chroma(
            persist_directory=DB_PATH,
            embedding_function=embedding_model,
            collection_name=COLLECTION_NAME,
        )

    print("📄 Indexing document...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=[".\n\n", ".\r\n\r\n", "\n\n", "\r\n\r\n", ".\n", ".\r\n"],
        chunk_size=240,
        chunk_overlap=90,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    chroma_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME,
    )
    chroma_db.persist()
    print("✅ Document indexing complete!")
    return chroma_db


def format_faq_response(result):
    answer = result["result"]
    sources = result.get("source_documents", [])
    pages = {doc.metadata.get("page", -1) + 1 for doc in sources if "page" in doc.metadata}
    citation = f" (source: BonBon FAQ.pdf page {', '.join(map(str, sorted(pages)))})" if pages else ""
    return answer + citation


def create_agent():
    llm = ChatOllama(model="phi3", base_url="http://ollama:11434")
    chroma_db = load_or_create_chroma_db()
    retriever = chroma_db.as_retriever(search_kwargs={"k": 3})

    faq_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    kb_tool = Tool(
        name="Knowledge Base Search",
        func=lambda q: format_faq_response(faq_chain.invoke({"query": q})),
        description="Use this to answer questions about BonBon FAQ topics like internet, printer, or malware."
    )

    internet_tool = DuckDuckGoSearchRun()

    return initialize_agent(
        tools=[kb_tool, internet_tool],
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        verbose=False,
        handle_parsing_errors=True
    )


def main():
    agent = create_agent()
    print("\n🤖 Chatbot ready! Ask a question (type 'exit' to quit)", flush=True)
    while True:
        query = input("🧑 You: ").strip()
        if query.lower() == "exit":
            print("👋 Goodbye!")
            break
        try:
            print("🤖 Bot is thinking...", end="", flush=True)
            response = agent.invoke({"input": query})
            print("\r🤖 Bot:", response["output"])
        except Exception as e:
            print("\n⚠️ Error:", e)


if __name__ == "__main__":
    main()
