# AI Research Agent

An AI-powered research agent that performs structured research using planning, retrieval, validation, and synthesis workflows.

The system takes a user query, generates a research strategy, retrieves relevant information from the web, validates sources, synthesizes findings, and returns a structured response.

---

# Features

* Query planning using LLMs
* Multi-step orchestration workflow
* Web search and retrieval
* Web scraping with retry logic and exponential backoff
* Source validation and filtering
* Dynamic agent decision making
* Structured synthesis of findings
* Confidence estimation based on retrieval quality
* Graceful degradation and fallback handling
* Dependency injection for improved testability
* FastAPI API interface
* Pydantic schema validation
* Pytest-based unit testing

---

# Architecture

```text
User Query
    ↓
Planner
    ↓
Search Tool
    ↓
Scraper Tool
    ↓
Validator Tool
    ↓
Synthesizer
    ↓
Structured Response
```

---

# Components

## Planner

The planner converts a user question into a structured research strategy.

Responsibilities:

* Identify task type
* Generate search queries
* Identify required information

Example:

Input:

```text
Compare top vector databases for RAG
```

Planner Output:

```json
{
  "task_type": "comparison",
  "search_queries": [
    "Pinecone vs Weaviate vs Qdrant comparison",
    "Milvus vs Pinecone benchmark"
  ],
  "required_information": [
    "performance",
    "pricing",
    "scalability",
    "RAG suitability"
  ]
}
```

---

## Search Tool

The search tool retrieves relevant URLs from the web.

Responsibilities:

* Retrieve relevant sources
* Reduce noisy retrieval
* Improve evidence quality

---

## Scraper Tool

The scraper extracts webpage content for downstream synthesis.

Responsibilities:

* Extract readable article content
* Handle failed requests gracefully
* Retry transient failures

Implemented Reliability Features:

* Retry Logic
* Exponential Backoff
* Timeout Handling

Example Retry Flow:

```text
Request Failed
    ↓
Retry 1 (1 second)
    ↓
Retry 2 (2 seconds)
    ↓
Retry 3 (4 seconds)
    ↓
Failure Returned Safely
```

---

## Validator Tool

The validator filters weak or noisy sources.

Validation checks:

* Empty content rejection
* Minimum content length checks
* Spam content filtering
* Low-quality source filtering

This reduces irrelevant information entering synthesis.

---

## Synthesizer

The synthesizer combines validated content into a structured research response.

Responsibilities:

* Cross-source reasoning
* Comparison-aware synthesis
* Tradeoff analysis
* Structured JSON generation

Output Format:

```json
{
  "question": "...",
  "short_answer": "...",
  "key_findings": [],
  "sources_used": [],
  "confidence": "...",
  "limitations": [],
  "suggested_next_steps": []
}
```

---

# Reliability & Production Readiness

## Retry Logic

The scraper retries failed requests up to three times using exponential backoff.

Handled Scenarios:

* HTTP 403 responses
* Timeouts
* Temporary network failures

If all retries fail, the workflow continues safely.

---

## Graceful Degradation

The planner and synthesizer include fallback behavior.

If:

* JSON parsing fails
* Provider errors occur
* Rate limits occur

the system falls back to a minimal structured plan rather than terminating.

---

## Dependency Injection

The Groq client is injected into planner and synthesizer components instead of being instantiated globally.

Benefits:

* Improved testability
* Easier mocking
* Better modularity
* Easier future provider replacement

---

# Adaptive Agent Behaviour

The agent is not strictly linear.

After retrieval, the orchestrator evaluates evidence quality.

If fewer than two validated sources are collected, the agent dynamically expands retrieval before synthesis.

Examples:

* Comparison Tasks → Benchmark Search
* Recommendation Tasks → Review Search
* Analysis Tasks → Analysis-Focused Search

This improves evidence coverage and final answer quality.

---

# Hallucination Reduction Strategy

The project reduces hallucinations through multiple safeguards.

## Retrieval Grounding

The system retrieves external evidence before generating answers.

```text
User Query
    ↓
Retrieval
    ↓
Validation
    ↓
Synthesis
```

## Planning Layer

The planner transforms broad questions into focused search queries.

Example:

Instead of:

```text
vector databases
```

The planner generates:

```text
Pinecone vs Weaviate vs Qdrant comparison
Milvus vs Pinecone benchmark
```

This improves retrieval quality.

---

## Source Validation

The validator removes:

* Empty pages
* Spam content
* Low-quality retrieval
* Weak evidence

---

## Structured Outputs

Pydantic schemas enforce deterministic output formats.

---

## Confidence Estimation

Confidence is derived from retrieval quality.

| Valid Sources | Confidence |
| ------------- | ---------- |
| 1             | Low        |
| 2             | Medium     |
| 3+            | High       |

This prevents overconfident responses from weak retrieval.

---

# Testing

The project uses pytest for automated testing.

Covered Components:

* Validator Tool
* Scraper Tool
* Orchestrator Workflow

Testing Features:

* Assertions
* Mocking
* Offline execution

Run Tests:

```bash
python -m pytest
```

Current Result:

```text
5 passed
0 failed
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

## AI / LLM

* Groq API
* Llama 3.1

## Libraries

* requests
* BeautifulSoup4
* Pydantic
* python-dotenv
* pytest

---

# Project Structure

```text
research-agent/
│
├── app/
│   ├── main.py
│   ├── planner.py
│   ├── orchestrator.py
│   ├── synthesizer.py
│   ├── schemas.py
│   │
│   └── tools/
│       ├── search_tool.py
│       ├── scraper_tool.py
│       └── validator_tool.py
│
├── tests/
│   ├── test_orchestrator.py
│   ├── test_scraper.py
│   └── test_validator.py
│
├── screenshots/
├── Evaluation.md
├── requirements.txt
└── README.md
```

---

# Setup

Clone Repository:

```bash
git clone <repo-url>
cd research-agent
```

Create Virtual Environment:

```bash
python -m venv venv
```

Activate Environment:

Windows:

```bash
venv\Scripts\activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Start API:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Evaluation

Detailed evaluation results are available in:

```text
Evaluation.md
```

The evaluation includes:

* Successful research tasks
* Retry logic evidence
* Dynamic agent behaviour
* Failure case analysis
* Hallucination mitigation strategy

---

# Known Limitations

* Some websites block scraping (403 responses)
* Retrieval quality depends on public source availability
* Confidence uses heuristic scoring
* The system currently relies on a single LLM provider
* LLM outputs remain probabilistic

---

# Future Improvements

* Multi-provider LLM fallback
* Semantic source ranking
* Retrieval caching
* Async orchestration
* Enhanced confidence estimation
* Larger evaluation benchmarks

---

# Example Output

```json
{
  "question": "Compare top vector databases for RAG",
  "short_answer": "Pinecone is best for managed production deployments, Qdrant is lightweight and startup-friendly, Weaviate supports hybrid search, while Milvus is suitable for enterprise-scale workloads.",
  "confidence": "High"
}
```
