# Cost-Optimized Serverless RAG Pipeline using BigQuery Vector Search and Gemini

## Overview

This project demonstrates how to build a production-style Retrieval-Augmented Generation (RAG) system using Google Cloud Platform. Financial documents (SEC 10-K reports or annual reports) are transformed into vector embeddings, stored in BigQuery, and queried using semantic search. Retrieved document chunks are provided to Gemini to generate grounded answers.

---

## Features

- PDF document ingestion
- Intelligent text chunking using LangChain
- Vertex AI text embeddings
- BigQuery Vector Search
- Gemini 2.5 Flash for grounded responses
- Cost-optimized serverless architecture
- End-to-end Retrieval-Augmented Generation pipeline

---

## Architecture

```text
PDF Documents
      │
      ▼
Google Cloud Storage
      │
      ▼
LangChain Loader
      │
      ▼
Text Splitter
      │
      ▼
Vertex AI Embeddings
      │
      ▼
BigQuery Vector Database
──────────────────────────────
      │
User Question
      │
      ▼
Question Embedding
      │
      ▼
BigQuery VECTOR_SEARCH
      │
      ▼
Relevant Context
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Grounded Answer
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Programming | Python 3.10 |
| Framework | LangChain |
| LLM | Gemini 2.5 Flash |
| Embeddings | Vertex AI Text Embedding |
| Vector Database | BigQuery Vector Search |
| Storage | Google Cloud Storage |
| Cloud Platform | Google Cloud Platform |

---

## Project Structure

```text
src/
    test_setup.py
    ingest_data.py
    embedded_store.py
    query_rag.py

requirements.txt

README.md
```

---

## Pipeline

### Phase 1: Knowledge Base

- Upload PDFs
- Load documents
- Split into chunks
- Generate embeddings
- Store vectors in BigQuery

### Phase 2: Retrieval

- Embed user question
- Search BigQuery using VECTOR_SEARCH
- Retrieve top-k relevant chunks
- Send grounded prompt to Gemini
- Generate answer

---

## Example Query

```
What is the company's strategy regarding enterprise infrastructure and AI?
```

---

## Example Output

```
According to the annual report, the company plans to expand enterprise AI capabilities by investing in cloud infrastructure, AI-driven automation, and strategic partnerships...
```

---

## Future Improvements

- Streamlit web interface
- FastAPI REST API
- Batch document ingestion
- Hybrid Search (Keyword + Vector)
- Citation highlighting
- Multi-document support
- Docker deployment
- CI/CD with GitHub Actions

---

## Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Large Language Models (LLMs)
- Google Cloud Platform
- BigQuery Vector Search
- Vertex AI
- LangChain
- Prompt Engineering
- Data Engineering
- Python

---

## License

MIT License