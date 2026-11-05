from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from common import get_llm


def write_email(purpose: str, recipient: str, tone: str, details: str, length: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You write clear, professional emails. Output a subject line "
                   "followed by the email body. No extra commentary."),
        ("human", "Purpose: {purpose}\nRecipient: {recipient}\nTone: {tone}\n"
                  "Length: {length}\nKey details: {details}"),
    ])
    chain = prompt | get_llm(0.7) | StrOutputParser()
    return chain.invoke(dict(purpose=purpose, recipient=recipient, tone=tone,
                             details=details, length=length))
