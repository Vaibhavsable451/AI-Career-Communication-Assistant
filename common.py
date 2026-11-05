import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pypdf import PdfReader

load_dotenv()
MODEL = "openai/gpt-oss-120b"


def get_llm(temperature: float = 0.2) -> ChatGroq:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY missing. Add it to a .env file.")
    return ChatGroq(model=MODEL, temperature=temperature, api_key=key)


def read_pdf(file) -> str:
    reader = PdfReader(file)
    return "\n".join((p.extract_text() or "") for p in reader.pages)
