from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from common import get_llm


class ResumeProfile(BaseModel):
    name: str = Field(description="Candidate name")
    email: str = Field(default="", description="Email if present")
    technical_skills: List[str]
    soft_skills: List[str]
    years_experience: float = Field(description="Approx. total years of experience")
    education: List[str]
    summary: str = Field(description="2-3 sentence professional summary")
    strengths: List[str]
    improvements: List[str] = Field(description="Suggestions to improve the resume")


def analyze_resume(resume_text: str) -> ResumeProfile:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter. Extract structured info "
                   "from the resume. Do not invent facts."),
        ("human", "Resume:\n\n{resume}"),
    ])
    chain = prompt | get_llm(0).with_structured_output(ResumeProfile)
    return chain.invoke({"resume": resume_text})
