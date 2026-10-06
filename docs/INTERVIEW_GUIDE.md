# Interview Guide
## What is DocMind AI?
A document intelligence web app that lets authenticated users upload PDF/DOCX files and ask grounded questions, summarize, extract facts and compare documents.

## Why build it?
Long documents are slow to search manually. The project turns them into an evidence-grounded knowledge workspace.

## Why Python / Flask / MySQL?
Python has strong document/AI libraries; Flask keeps the backend understandable and modular; MySQL fits relational users, documents, chats and history.

## RAG / embeddings / vector search
RAG retrieves relevant evidence before generation. Embeddings are numeric semantic representations. Similarity search finds chunks closest to a question, so the LLM receives focused context rather than an entire document.

## RAG vs normal LLM
A normal LLM may answer from general training. RAG injects private/recent document evidence and can expose sources.

## Upload and extraction
The backend validates PDF/DOCX, saves a secure randomized filename, extracts text per page where possible, normalizes it and creates overlapping chunks.

## Chunking
Chunks keep prompts manageable and retrieval precise. Overlap reduces loss of context at boundaries.

## Hallucination reduction
Retrieve relevant chunks, instruct the model to use only context, return an insufficient-information response when retrieval is weak, and expose sources.

## Authentication
Passwords are hashed. Login returns JWT. Protected endpoints derive the user ID from JWT and filter resources by owner.

## Database relationships
User → Documents/Chats; Document → Chunks/Summaries; Chat → Messages.

## Challenges
Reliable text extraction, chunk sizing, retrieval relevance, secure multi-user ownership and external API failures.

## Security
Hashed passwords, JWT, ORM, ownership checks, secure filenames, extension/size limits, environment secrets.

## Future improvements
Persistent vector indexes, OCR, async processing, streaming, reranking, evaluation and richer provider abstraction.

## Likely questions
**Why not ChatGPT directly?** DocMind adds private document lifecycle, retrieval, ownership, history, structured workflows and evidence references.
**Why overlap chunks?** To preserve context crossing chunk boundaries.
**What if answer is absent?** The system should say insufficient information instead of inventing it.
**Why relational DB?** Core entities and ownership/history have clear relationships and integrity constraints.
