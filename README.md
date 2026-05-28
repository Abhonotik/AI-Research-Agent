# AI Research Agent

An AI-powered research agent that performs structured research using planning, retrieval, validation, and synthesis workflows.

The system takes a user query, generates a research strategy, retrieves relevant information from the web, validates sources, synthesizes findings, and returns a structured response.

---

## Features

* Query planning using LLMs
* Multi-step orchestration workflow
* Web search and retrieval
* Web scraping for content extraction
* Source validation and filtering
* Structured synthesis of findings
* Confidence estimation based on retrieval quality
* FastAPI API interface
* Pydantic schema validation

---

## Architecture

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

### Planner

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

Planner output:

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

### Search Tool

The search tool retrieves relevant URLs from the web.

Goals:

* Retrieve relevant sources
* Reduce noisy retrieval
* Prioritize comparison-oriented pages

Filtering heuristics:

* comparison
* vs
* benchmark
* best
* top

---

### Scraper Tool

The scraper extracts webpage content for downstream synthesis.

Responsibilities:

* Extract readable article text
* Remove webpage noise
* Handle failed requests gracefully

---

### Validator Tool

The validator filters weak or noisy sources.

Validation checks:

* Empty content rejection
* Minimum content length
* Low-quality/noisy page filtering

This helps reduce hallucinations and irrelevant synthesis.

---

### Synthesizer

The synthesizer combines validated research content into a structured response.

Responsibilities:

* Cross-source synthesis
* Comparison-aware reasoning
* Tradeoff analysis
* Structured JSON generation

Output format:

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

## Hallucination Reduction Strategy

Hallucinations cannot be fully eliminated in probabilistic systems, but they can be reduced.

This project reduces hallucinations using:

1. Retrieval grounding
   The model answers using retrieved information rather than relying only on internal memory.

2. Planning layer
   The planner improves retrieval quality through structured search strategies.

3. Source validation
   Noisy or irrelevant sources are filtered before synthesis.

4. Structured outputs
   Pydantic schemas enforce deterministic output formatting.

5. Confidence estimation
   Confidence is derived from retrieval quality rather than relying purely on model self-confidence.

---

## Confidence Heuristic

Confidence is calculated using validated retrieval quality.

| Valid Sources | Confidence |
| ------------- | ---------- |
| 1             | Low        |
| 2             | Medium     |
| 3+            | High       |

This avoids relying entirely on model self-assessment.

---

## Tech Stack

Backend:

* Python
* FastAPI
* Uvicorn

AI / LLM:

* Groq API
* Llama 3.1

Libraries:

* requests
* BeautifulSoup4
* Pydantic
* python-dotenv

---

## Project Structure

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
├── test_planner.py
├── test_search.py
├── test_scraper.py
├── test_validator.py
├── test_synthesizer.py
├── test_orchestrator.py
│
├── requirements.txt
└── README.md
```

---

## API Usage

Run server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Example request:

```json
{
  "query": "Compare top vector databases for RAG"
}
```

---

## Setup

Clone repository:

```bash
git clone <repo-url>
cd research-agent
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Start server:

```bash
uvicorn app.main:app --reload
```

---

## Limitations

* Web scraping quality depends on page structure
* Search relevance may vary
* Confidence uses heuristic scoring
* Retrieval quality affects synthesis quality
* LLM outputs remain probabilistic

---

## Future Improvements

* Retry logic
* Better source ranking
* Smarter confidence scoring
* Async orchestration
* Multi-agent workflows
* Retrieval caching

---

## Example Output

```json
{
  "question": "Compare top vector databases for RAG",
  "short_answer": "Pinecone is best for managed production deployments, Qdrant is lightweight and startup-friendly, Weaviate supports hybrid search, while Milvus is suitable for enterprise-scale workloads.",
  "confidence": "Medium"
}
```
