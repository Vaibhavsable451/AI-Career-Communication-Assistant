# AI Career & Communication Assistant

An AI-powered Career & Communication Assistant built with Groq, LangChain, and LangGraph.

Model: `openai/gpt-oss-120b` via Groq.

## Features
- **Smart Email Writer**: Generate professional emails with customizable tone and intent.
- **Resume Analyzer**: Extract key skills, evaluate strengths/weaknesses, and receive recommendations.
- **Job Description Matcher**: Compare your resume against target JDs with fit scores and gap analysis.
- **PDF Q&A Chatbot**: Chat with career documents and resumes directly.
- **Spam & Phishing Detector**: Analyze suspicious emails and job offers for threats.
- **Customer Support Agent**: Automated support bot using LangGraph workflows.

## Setup
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # then put your GROQ_API_KEY inside
streamlit run app.py
```
Get a free key at https://console.groq.com/keys
