# DocMind AI
AI-powered document intelligence platform for PDF/DOCX upload, grounded RAG Q&A, summaries, structured extraction and document comparison.

## Problem
Knowledge is trapped in long documents. DocMind turns private uploaded documents into a searchable, source-grounded workspace.

## Stack
Python, Flask, JWT, SQLAlchemy, MySQL, React/Vite, PyMuPDF, python-docx, Sentence Transformers, LLM API.

## Architecture
React → Flask REST API → MySQL + document processing → embeddings/retrieval → LLM → grounded response + sources.

## Windows setup
1. MySQL: `CREATE DATABASE docmind_ai;`
2. `cd backend`
3. `py -m venv venv`
4. `venv\Scripts\activate`
5. `pip install -r requirements.txt`
6. Copy `.env.example` to `.env`, set `DATABASE_URL`, `JWT_SECRET_KEY`, `LLM_API_KEY`.
7. `py run.py`
8. New terminal: `cd frontend`
9. `npm install`
10. `npm run dev`

Backend: http://localhost:5000 | Frontend: Vite URL (usually http://localhost:5173)

## RAG workflow
Upload → extract → clean/chunk → embedding similarity retrieval → controlled context → LLM → answer with document/page sources.

## Features
Authentication, ownership isolation, PDF/DOCX upload, search/list/delete, RAG Q&A, chat history API, summaries, extraction, multi-document Q&A, two-document comparison, dashboard, responsive UI.

## API overview
`POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `GET/POST /api/documents`, `DELETE /api/documents/:id`, `POST /api/ai/ask`, `/summarize`, `/extract`, `/compare`, `GET /api/chats`.

## Screenshots
Add screenshots after running locally to `docs/screenshots/`.

## Troubleshooting
- MySQL connection error: verify DATABASE_URL and MySQL service.
- AI 503: set a valid LLM_API_KEY and compatible LLM_MODEL/base URL.
- First semantic search may download the embedding model.

## Interview pitch
DocMind is not a generic chatbot: it combines authenticated document management with retrieval over user-owned content, then constrains the LLM to retrieved evidence and returns source/page references.

## Future improvements
Persistent FAISS/Chroma indexes, OCR for scanned PDFs, streaming answers, background jobs, provider adapters, richer citations and evaluation metrics.
