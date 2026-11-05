"""Customer support chatbot using LangGraph with per-session memory."""
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from common import get_llm

# Edit this knowledge base for your own business.
KNOWLEDGE_BASE = """
Company: ShopEasy
- Shipping: 3-5 business days; free over $50.
- Returns: within 30 days, item unused, original packaging.
- Refunds: processed in 5-7 business days after we receive the return.
- Support hours: Mon-Fri 9am-6pm. Email: support@shopeasy.example
- Order tracking: via the link in the confirmation email.
"""

SYSTEM = SystemMessage(content=(
    "You are a friendly customer support agent. Use ONLY the knowledge base below. "
    "If you don't know, apologise and offer to escalate to a human at the support email.\n"
    f"{KNOWLEDGE_BASE}"))


def chatbot(state: MessagesState):
    reply = get_llm(0.3).invoke([SYSTEM] + state["messages"])
    return {"messages": [reply]}


_g = StateGraph(MessagesState)
_g.add_node("chatbot", chatbot)
_g.add_edge(START, "chatbot")
_g.add_edge("chatbot", END)
app_graph = _g.compile(checkpointer=MemorySaver())


def chat(message: str, thread_id: str) -> str:
    out = app_graph.invoke({"messages": [("user", message)]},
                           config={"configurable": {"thread_id": thread_id}})
    return out["messages"][-1].content
