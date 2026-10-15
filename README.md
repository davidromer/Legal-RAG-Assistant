# Legal-RAG-Assistant

AI-powered legal document assistant built with Python, FastAPI, PostgreSQL/pgvector
and LLMs. It enables semantic search and question answering over legal documents
while returning source-grounded responses with citations.

## Problem
Legal teams lose hours searching contracts and rulings manually. This assistant
indexes legal documents and answers natural-language questions, always citing
the exact document, page and fragment — and explicitly refuses to answer when
there isn't enough evidence.

## Architecture
PDF/DOCX → extraction → cleaning/chunking → embeddings → PostgreSQL+pgvector
→ retriever → LLM → cited answer. See `/docs/architecture.png`.

## Stack
Python · FastAPI · PostgreSQL · pgvector · OpenAI embeddings · Docker · pytest

## Demo
```bash
docker compose up --build
curl -F "archivo=@contrato.pdf" http://localhost:8000/documents
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuál es la cláusula de terminación?"}'
```

## Evaluation
Retrieval hit rate, context relevance and answer faithfulness measured against
a 25-question labeled dataset. See `/scripts/eval_retrieval.py`.
