# 🧠 DocMind AI

### AI-Powered Document Intelligence & Knowledge Platform

DocMind AI is a full-stack document intelligence platform that allows users to upload PDF and DOCX documents, ask questions using Retrieval-Augmented Generation (RAG), generate summaries, extract structured information, compare documents, and review previous AI conversations.

The system grounds AI responses in user-uploaded documents and provides source/page references to make answers more transparent and useful.

---

## 🚀 Key Features

- 🔐 User Registration & Login with JWT Authentication
- 📄 PDF and DOCX Document Upload
- 📝 Automatic Text Extraction
- ✂️ Document Chunking
- 🧠 Semantic Search using Sentence Transformers
- 🤖 Gemini-powered AI Responses
- 🔎 Retrieval-Augmented Generation (RAG)
- 📚 Multi-Document Question Answering
- 🔗 Source and Page Citations
- 📋 AI Document Summarization
- 💾 Cached Summaries to Reduce AI API Usage
- 📊 Structured Information Extraction
- ⇄ Two-Document AI Comparison
- 💬 Chat History
- 🗑️ Document Management and Deletion
- 👤 Per-User Document Isolation
- 📱 Responsive React Dashboard

---

## 🎯 Problem Statement

Important information is often buried inside long documents, making manual searching and comparison time-consuming.

DocMind AI converts uploaded documents into an intelligent knowledge workspace where users can:

- Ask questions about document content
- Retrieve semantically relevant information
- Generate concise summaries
- Extract important facts and entities
- Compare two documents
- Trace answers back to their source documents and pages

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Axios

### Backend

- Python
- Flask
- Flask-JWT-Extended
- Flask-CORS
- SQLAlchemy

### Database

- MySQL

### AI & NLP

- Google Gemini API
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Retrieval-Augmented Generation (RAG)
- Semantic Similarity Search

### Document Processing

- PyMuPDF
- python-docx

---

## 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │     React Frontend   │
                │   User Interface     │
                └──────────┬───────────┘
                           │
                           │ REST API
                           ▼
                ┌──────────────────────┐
                │     Flask Backend    │
                │ Authentication/API   │
                └──────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       ┌──────────┐  ┌───────────┐  ┌──────────┐
       │  MySQL   │  │ Document  │  │   RAG    │
       │ Database │  │Processing │  │ Retrieval│
       └──────────┘  └───────────┘  └────┬─────┘
                                         │
                                         ▼
                               ┌──────────────────┐
                               │   Gemini API     │
                               │ Grounded Answer  │
                               └──────────────────┘
```

---

## 🧠 RAG Workflow

DocMind AI uses Retrieval-Augmented Generation instead of sending an entire document directly to the LLM.

```text
Upload PDF / DOCX
        ↓
Validate Document
        ↓
Extract Text
        ↓
Clean and Chunk Text
        ↓
Generate Embeddings
        ↓
User Asks Question
        ↓
Semantic Similarity Search
        ↓
Retrieve Relevant Chunks
        ↓
Verify User Document Access
        ↓
Build Controlled Context
        ↓
Send Context + Question to Gemini
        ↓
Generate Grounded Answer
        ↓
Return Answer + Source/Page Citations
```

This architecture helps reduce irrelevant context and keeps responses grounded in the selected documents.

---

## 🔐 Security

DocMind AI includes several application-level security mechanisms:

- JWT-based authentication
- Protected API endpoints
- Per-user document ownership
- Document access validation before AI processing
- Environment variables for secrets
- API keys excluded from Git using `.gitignore`
- Password hashing
- Input and document validation
- Token-expiry handling

> Never commit your real `.env` file, Gemini API key, JWT secret, or database password to GitHub.

---

## 📁 Project Structure

```text
DocMind-AI/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── ai.py
│   │   │   ├── chats.py
│   │   │   └── dashboard.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── llm_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   ├── utils/
│   │   ├── models.py
│   │   ├── config.py
│   │   └── extensions.py
│   │
│   ├── tests/
│   ├── uploads/
│   ├── vector_store/
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── api.js
│   │   └── style.css
│   │
│   ├── package.json
│   └── .env.example
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_DESIGN.md
│   ├── INTERVIEW_GUIDE.md
│   └── RAG_EXPLANATION.md
│
├── sample_data/
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

Install:

- Python 3
- Node.js and npm
- MySQL 8+
- Git

---

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd DocMind-AI
```

---

### 2. Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE docmind_ai;
```

---

### 3. Backend Setup

```powershell
cd backend

py -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env` from `.env.example`.

Example:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/docmind_ai

JWT_SECRET_KEY=YOUR_STRONG_SECRET_KEY

LLM_API_KEY=YOUR_GEMINI_API_KEY

MAX_UPLOAD_MB=15
```

Do not use these placeholder values in production.

Start the backend:

```powershell
py run.py
```

Backend runs at:

```text
http://127.0.0.1:5000
```

---

### 4. Frontend Setup

Open another terminal:

```powershell
cd frontend

npm install

npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

---

## 🔌 API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Current user |
| GET | `/api/documents` | List user documents |
| POST | `/api/documents/upload` | Upload document |
| DELETE | `/api/documents/:id` | Delete document |
| POST | `/api/ai/ask` | RAG-based Q&A |
| POST | `/api/ai/summarize` | Generate/load document summary |
| POST | `/api/ai/extract` | Extract structured information |
| POST | `/api/ai/compare` | Compare two documents |
| GET | `/api/chats` | Chat history |
| GET | `/api/chats/:id/messages` | Previous chat messages |

---

## 📋 AI Summarization & Caching

DocMind AI stores successfully generated summaries in MySQL.

```text
User requests summary
        ↓
Check saved summary
        ↓
     Exists?
     ↙    ↘
   Yes     No
    ↓       ↓
 Return   Gemini API
 cached      ↓
 summary   Generate
             ↓
          Save in DB
             ↓
          Return summary
```

This reduces repeated API requests and improves response time for previously summarized documents.

---

## 🔍 Grounded AI Responses

DocMind AI is designed to avoid behaving like a generic chatbot.

For document Q&A, the system:

1. Searches the selected user's documents.
2. Retrieves semantically relevant chunks.
3. Sends only retrieved context to the LLM.
4. Instructs the model not to invent unsupported information.
5. Returns document and page references with the answer.

If sufficient information cannot be found, the system can respond that the selected documents do not contain enough information.

---

## 📊 Database

Main tables include:

```text
user
document
document_chunk
chat
message
summary
```

These tables store user accounts, document metadata, extracted chunks, conversation history, messages and cached summaries.

See:

```text
docs/DATABASE_DESIGN.md
```

for additional database documentation.

---

## 📸 Screenshots

Project screenshots can be stored in:

```text
docs/screenshots/
```

Recommended screenshots:

- Login / Registration
- Dashboard
- Document Upload
- Documents
- AI Chat with Citations
- Document Summary
- Chat History
- Document Comparison

---

## ⚠️ AI API Limits

DocMind uses an external LLM API for AI generation.

API providers may enforce request or usage quotas. The application handles AI service failures with user-friendly error messages.

Successfully generated document summaries can be cached in MySQL to reduce repeated AI API usage.

---

## 🧪 Testing

The project has been tested for:

- User registration and login
- JWT-protected routes
- Document upload
- PDF text extraction
- Document chunking
- Semantic retrieval
- RAG Q&A
- Unsupported-question handling
- Source/page citations
- Multi-document retrieval
- Document comparison
- Chat history
- Document deletion
- Per-user data isolation
- Token-expiry handling

---

## 💡 Why DocMind AI?

DocMind is not intended to replace general-purpose AI assistants.

It demonstrates how LLMs can be integrated into an application where AI responses are grounded in private, user-owned documents.

The project combines:

```text
Full-Stack Development
        +
Database Design
        +
Authentication
        +
Document Processing
        +
Semantic Search
        +
RAG
        +
LLM Integration
```

---

## 🎤 Interview Explanation

> **“DocMind AI is a full-stack document intelligence platform that I built using React, Flask and MySQL. Users can upload PDF or DOCX documents, and the backend extracts and chunks their content. For document Q&A, I use Sentence Transformers to perform semantic retrieval and select relevant chunks. Those chunks are provided as controlled context to Gemini, which generates a grounded answer. The system also returns document and page citations. I implemented JWT authentication and document ownership checks so users can only access their own data. The application also supports document summarization, structured extraction, chat history and document comparison.”**

---

## 🔮 Future Improvements

- OCR support for scanned documents
- Persistent vector database such as FAISS/Chroma
- Streaming AI responses
- Background document-processing jobs
- Improved multi-document retrieval/reranking
- Additional LLM provider adapters
- Advanced citation highlighting
- RAG evaluation metrics
- Production deployment and monitoring

---

## 👨‍💻 Author

**Mukund Kumar Jha**

MCA Student | Full-Stack / Backend Developer

GitHub: `Mukund9128`

---

## ⭐ Project Status

**Core development complete.**

Current focus:

- Final testing
- Documentation
- Deployment preparation
- UI/demo refinement