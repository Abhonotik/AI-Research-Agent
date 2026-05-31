from pydantic import BaseModel # proper output in strict structure. 
from typing import Literal # for fixed options only.
from typing import List # only list of items, no single values allowed or number. 


# for the input query, which is a string.
class QueryRequest(BaseModel): 
    query: str


# for the research plan, which includes the task type, search queries, and required information.
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