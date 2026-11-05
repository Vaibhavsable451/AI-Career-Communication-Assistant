from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from common import get_llm, read_pdf


def build_index(files):
    text = "\n".join(read_pdf(f) for f in files)
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_text(text)
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, emb)


def answer(vectorstore, question: str) -> str:
    docs = vectorstore.similarity_search(question, k=4)
    context = "\n\n---\n\n".join(d.page_content for d in docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer ONLY from the context. If the answer is not there, say "
                   "you couldn't find it in the PDF.\n\nContext:\n{context}"),
        ("human", "{question}"),
    ])
    chain = prompt | get_llm(0) | StrOutputParser()
    return chain.invoke({"context": context, "question": question})
