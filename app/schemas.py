from pydantic import BaseModel
from typing import Literal
from typing import List


class QueryRequest(BaseModel):
    query: str


class ResearchPlan(BaseModel):
    task_type: str
    search_queries: List[str]
    required_information: List[str]


class ResearchResponse(BaseModel):
    question: str
    short_answer: str
    key_findings: List[str]
    sources_used: List[str]
    confidence: Literal["Low", "Medium", "High"]
    limitations: List[str]
    suggested_next_steps: List[str]