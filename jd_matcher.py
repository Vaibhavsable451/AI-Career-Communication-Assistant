from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from common import get_llm


class MatchResult(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall match score 0-100")
    matched_skills: List[str]
    missing_skills: List[str]
    verdict: str = Field(description="Strong / Moderate / Weak match with one-line reason")
    suggestions: List[str] = Field(description="How the candidate can close the gaps")


def match_resume_to_jd(resume: str, jd: str) -> MatchResult:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a strict ATS and hiring expert. Compare the resume to the "
                   "job description and score fairly."),
        ("human", "JOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"),
    ])
    chain = prompt | get_llm(0).with_structured_output(MatchResult)
    return chain.invoke({"jd": jd, "resume": resume})
