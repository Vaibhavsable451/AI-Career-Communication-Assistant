"""LangGraph pipeline: extract signals -> classify -> final report."""
import re
from typing import List, TypedDict
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from common import get_llm


class Verdict(BaseModel):
    label: str = Field(description="One of: Safe, Spam, Phishing")
    confidence: int = Field(ge=0, le=100)
    reasons: List[str]
    recommended_action: str


class State(TypedDict, total=False):
    email: str
    signals: dict
    verdict: Verdict


URGENT = ["urgent", "immediately", "act now", "verify your account", "suspended",
          "password", "limited time", "winner", "click here", "gift card", "wire transfer"]


def extract_signals(state: State) -> State:
    text = state["email"]
    links = re.findall(r"https?://\S+", text)
    signals = {
        "links": links,
        "ip_links": [l for l in links if re.search(r"https?://\d+\.\d+\.\d+\.\d+", l)],
        "urgent_keywords": [k for k in URGENT if k in text.lower()],
        "all_caps_ratio": round(sum(c.isupper() for c in text) / max(len(text), 1), 2),
    }
    return {"signals": signals}


def classify(state: State) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an email security analyst. Classify the email as Safe, "
                   "Spam or Phishing using the text and the heuristic signals."),
        ("human", "EMAIL:\n{email}\n\nSIGNALS:\n{signals}"),
    ])
    chain = prompt | get_llm(0).with_structured_output(Verdict)
    return {"verdict": chain.invoke({"email": state["email"], "signals": state["signals"]})}


_graph = StateGraph(State)
_graph.add_node("extract_signals", extract_signals)
_graph.add_node("classify", classify)
_graph.add_edge(START, "extract_signals")
_graph.add_edge("extract_signals", "classify")
_graph.add_edge("classify", END)
detector = _graph.compile()


def detect(email: str) -> State:
    return detector.invoke({"email": email})
