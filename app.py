import uuid
import streamlit as st
from common import read_pdf
from resume_analyzer import analyze_resume
from jd_matcher import match_resume_to_jd
from email_writer import write_email
from spam_detector import detect
from pdf_chatbot import build_index, answer
from support_bot import chat

st.set_page_config(page_title="AI Projects (Groq)", page_icon="🤖", layout="wide")
from ui import CSS, hero
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(hero("🤖 AI Toolkit", "Resume · Jobs · Email · Spam · PDF · Support — powered by Groq, LangChain & LangGraph"),
            unsafe_allow_html=True)

with st.sidebar:
    import os
    st.header("⚙️ Settings")
    st.write("**Model:** `openai/gpt-oss-120b`")
    st.write("**API key:** " + ("✅ loaded" if os.getenv("GROQ_API_KEY") else "❌ missing (.env)"))
    st.caption("Built with Streamlit + LangChain + LangGraph")

tabs = st.tabs(["📄 Resume", "🎯 JD Match", "✉️ Email", "🛡️ Spam", "📚 PDF Chat", "💬 Support"])


def resume_input(key):
    f = st.file_uploader("Upload resume (PDF)", type="pdf", key=key + "f")
    txt = st.text_area("...or paste resume text", height=150, key=key + "t")
    return read_pdf(f) if f else txt


# 1. Resume Analyzer
with tabs[0]:
    resume = resume_input("r1")
    if st.button("Analyze", key="b1") and resume.strip():
        with st.spinner("Analyzing..."):
            p = analyze_resume(resume)
        st.subheader(p.name)
        st.write(p.summary)
        c1, c2 = st.columns(2)
        c1.markdown("**Technical skills**"); c1.write(", ".join(p.technical_skills))
        c2.markdown("**Soft skills**"); c2.write(", ".join(p.soft_skills))
        st.write(f"**Experience:** ~{p.years_experience} yrs · **Education:** {'; '.join(p.education)}")
        st.markdown("**Strengths**"); [st.write("- " + s) for s in p.strengths]
        st.markdown("**Improvements**"); [st.write("- " + s) for s in p.improvements]

# 2. JD Matcher
with tabs[1]:
    resume2 = resume_input("r2")
    jd = st.text_area("Job description", height=200)
    if st.button("Match", key="b2") and resume2.strip() and jd.strip():
        with st.spinner("Matching..."):
            m = match_resume_to_jd(resume2, jd)
        st.metric("Match score", f"{m.score}/100")
        st.progress(m.score / 100)
        st.write(m.verdict)
        c1, c2 = st.columns(2)
        c1.success("Matched: " + ", ".join(m.matched_skills))
        c2.error("Missing: " + ", ".join(m.missing_skills))
        st.markdown("**Suggestions**"); [st.write("- " + s) for s in m.suggestions]

# 3. Email Writer
with tabs[2]:
    purpose = st.text_input("Purpose", "Request a meeting")
    recipient = st.text_input("Recipient", "Hiring manager")
    c1, c2 = st.columns(2)
    tone = c1.selectbox("Tone", ["Professional", "Friendly", "Formal", "Persuasive", "Apologetic"])
    length = c2.selectbox("Length", ["Short", "Medium", "Long"])
    details = st.text_area("Key details", height=120)
    if st.button("Generate", key="b3"):
        with st.spinner("Writing..."):
            st.text_area("Result", write_email(purpose, recipient, tone, details, length), height=300)

# 4. Spam Detector
with tabs[3]:
    email = st.text_area("Paste email (with subject/sender)", height=250)
    if st.button("Scan", key="b4") and email.strip():
        with st.spinner("Scanning..."):
            r = detect(email)
        v = r["verdict"]
        (st.success if v.label == "Safe" else st.error)(f"{v.label} · {v.confidence}% confidence")
        st.markdown("**Reasons**"); [st.write("- " + x) for x in v.reasons]
        st.info("Action: " + v.recommended_action)
        with st.expander("Heuristic signals"):
            st.json(r["signals"])

# 5. PDF Chatbot
with tabs[4]:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="pdfs")
    if files and st.button("Process PDFs"):
        with st.spinner("Indexing..."):
            st.session_state.vs = build_index(files)
            st.session_state.pdf_msgs = []
        st.success("Ready! Ask questions below.")
    if "vs" in st.session_state:
        for role, msg in st.session_state.pdf_msgs:
            st.chat_message(role).write(msg)
        if q := st.chat_input("Ask about your PDF", key="pdfq"):
            st.chat_message("user").write(q)
            a = answer(st.session_state.vs, q)
            st.chat_message("assistant").write(a)
            st.session_state.pdf_msgs += [("user", q), ("assistant", a)]

# 6. Support Chatbot
with tabs[5]:
    st.session_state.setdefault("tid", str(uuid.uuid4()))
    st.session_state.setdefault("sup_msgs", [("assistant",
        "👋 Hi! I'm the ShopEasy assistant. Ask me about shipping, returns, refunds or order tracking.")])
    quick = ["How long is shipping?", "What's the return policy?", "When do I get my refund?", "Support hours?"]
    clicked = None
    for c, qq in zip(st.columns(4), quick):
        if c.button(qq, key="q_" + qq):
            clicked = qq
    for role, msg in st.session_state.sup_msgs:
        st.chat_message(role).write(msg)
    q = st.chat_input("How can we help?", key="supq") or clicked
    if q:
        st.chat_message("user").write(q)
        a = chat(q, st.session_state.tid)
        st.chat_message("assistant").write(a)
        st.session_state.sup_msgs += [("user", q), ("assistant", a)]