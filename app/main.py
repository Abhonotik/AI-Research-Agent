from fastapi import FastAPI
from pydantic import BaseModel

from app.orchestrator import run_research_agent


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():

    return {
        "message": "AI Research Agent Running"
    }


@app.post("/research")
def research(request: QueryRequest):

    response = run_research_agent(
        request.query
    )

    if not response:

        return {
            "status": "error",
            "message": "Research failed"
        }

    return response.model_dump()