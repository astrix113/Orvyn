# Orvyn 🤖✨

<div align="center">

![Orvyn Banner](https://img.shields.io/badge/Orvyn-AI%20Assistant-8B5CF6?style=for-the-badge&logo=rocket&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-FF6B6B?style=for-the-badge)

</div>

Orvyn is an intelligent, document-aware AI chat application built with FastAPI, LangGraph, and Google Gemini models. It supports conversational chat, uploaded document analysis with RAG, web search, calculator tools, and persistent memory for each conversation thread.

> 🚀 Think of Orvyn as a local AI workspace assistant that can chat, search uploaded files, remember facts, and answer with up-to-date web knowledge when needed.

---

## 🧭 Project Overview

Orvyn combines several modern AI building blocks:

- AI agent orchestration using LangGraph
- Streaming chat responses via FastAPI SSE
- Document ingestion and retrieval using Chroma + embeddings
- Search and browsing with Tavily
- Long-term per-thread memory in SQLite
- Conversation history and UI in a polished single-page web app

The app is built to feel like a lightweight ChatGPT-like interface, but with extra capabilities for private file knowledge and user-specific memory.

---

## ✨ Features

| Feature | Description | Status |
|---|---|---|
| Chat with Gemini | Streams AI responses in real time | ✅ |
| Multi-model selection | Supports multiple Gemini 2.5/3.x models | ✅ |
| Document upload | Accepts PDF, DOCX, TXT, MD, PY, and CSV files | ✅ |
| RAG retrieval | Searches uploaded files by semantic similarity | ✅ |
| Web search | Uses Tavily for current information | ✅ |
| Calculator | Performs simple math operations | ✅ |
| Memory | Saves and recalls user facts per thread | ✅ |
| Conversation history | Tracks previous chats and recent threads | ✅ |
| Docker-ready | Runs in a contained Python environment | ✅ |

---

## 🏗️ Architecture

```text
User Browser
    │
    ▼
FastAPI app (app.py)
    ├── LangGraph Agent (agent.py)
    │   ├── Gemini LLM
    │   ├── Tool calling
    │   ├── Web search
    │   └── Memory tools
    │
    ├── RAG Layer (rag.py)
    │   ├── File parsing
    │   ├── Chunking
    │   └── Chroma vector search
    │
    ├── SQLite storage (database.py)
    │   ├── Conversations
    │   ├── Messages
    │   └── Long-term memory
    │
    └── Static frontend (templates/index.html)
```

---

## 🧩 Core Components

### 1) Agent orchestration
Located in `agent.py`

- Builds the LangGraph workflow
- Binds tools to the Gemini model
- Chooses the correct model through normalization logic
- Uses a SQLite checkpoint database for conversation memory across steps

### 2) FastAPI backend
Located in `app.py`

Responsibilities:

- Serves the frontend at `/`
- Lists conversations via `/conversations`
- Fetches chat history via `/history/{thread_id}`
- Uploads files via `/upload`
- Streams chat responses via `/chat/stream`

### 3) RAG pipeline
Located in `rag.py`

Responsibilities:

- Reads supported uploaded file types
- Splits content into chunks
- Embeds text with Google Gemini embeddings
- Stores and retrieves document context from Chroma

### 4) Tools and actions
Located in `tools.py`

Included tools:

- `calculator` — safe simple math eval
- `search_uploaded_documents` — look through uploaded files
- `remember_this` — save facts to memory
- `recall_memory` — retrieve saved facts
- `web_search` — Tavily general web search

### 5) Persistence layer
Located in `database.py`

Stores:

- conversations
- chat messages
- long-term memory

Using SQLite so the app can keep thread-specific history without a heavy database setup.

---

## 📁 Project Structure

```text
Orvyn/
├── agent.py                  # LangGraph agent and Gemini model setup
├── app.py                   # FastAPI app + SSE chat endpoints
├── database.py              # SQLite models and session helpers
├── rag.py                   # Document upload, chunking, embeddings, retrieval
├── tools.py                 # Agent tools: calculator, memory, search, Tavily
├── requirements.txt         # Python package dependencies
├── Dockerfile               # Container config
├── templates/
│   └── index.html           # Frontend UI
├── public/                  # Static assets
├── uploads/                 # Uploaded files
├── data/                    # SQLite checkpoint + memory data
├── chroma_db/               # Chroma vector database persistence
├── test.py                  # Experimental/validation file
├── model_test.py            # Gemini model connectivity tests
├── .env                     # Local environment variables (not committed)
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

| Layer | Stack |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Agent Orchestration | LangGraph |
| LLM Provider | Google Gemini via `langchain-google-genai` |
| Search | Tavily |
| RAG | ChromaDB, LangChain embeddings, recursive chunking |
| File Parsing | PyPDF, docx2txt |
| Storage | SQLite |
| Frontend | Jinja2 + custom HTML/CSS/JS |
| Containerization | Docker |

---

## ⚙️ Environment Setup

Create a `.env` file in the project root with the following values:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_MODEL=gemini-2.5-flash
```

### Required API keys

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Required for Gemini LLM and embeddings |
| `TAVILY_API_KEY` | Required for live web search |
| `GEMINI_MODEL` | Optional override for the agent model |

> ⚠️ If the keys are missing, the app will fail when the relevant operations are invoked.

---

## ▶️ Running the Project

### Option 1: Local Python

```bash
pip install -r requirements.txt
python app.py
```

The app will run on:

```text
http://127.0.0.1:8080
```

### Option 2: Docker

```bash
docker build -t orvyn .
docker run -p 8080:8080 --env-file .env orvyn
```

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the UI |
| `/conversations` | GET | Lists conversation threads |
| `/history/{thread_id}` | GET | Fetches chat history for a thread |
| `/upload` | POST | Uploads and indexes a document |
| `/chat/stream` | POST | Streams chat responses |

### Example upload request

```bash
curl -X POST http://127.0.0.1:8080/upload \
  -F "thread_id=my-thread" \
  -F "file=@sample.pdf"
```

### Example chat request

```bash
curl -X POST http://127.0.0.1:8080/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Summarize the uploaded document",
    "thread_id": "my-thread",
    "model": "gemini-2.5-flash"
  }'
```

---

## 🧠 How the AI Works

Orvyn follows an agentic pattern:

1. The user sends a message from the frontend.
2. The LangGraph agent receives the message.
3. The system prompt instructs the model to use tools when needed.
4. The agent may call:
   - calculator
   - search_uploaded_documents
   - remember_this
   - recall_memory
   - Tavily web search
5. Responses are streamed back to the browser in real time.
6. Message and conversation state are saved to SQLite.

This makes the assistant more capable than a plain RAG bot by combining retrieval, search, memory, and tool use.

---

## 📦 Supported File Types

| Type | Supported |
|---|---|
| PDF | ✅ |
| DOCX | ✅ |
| TXT | ✅ |
| Markdown | ✅ |
| Python | ✅ |
| CSV | ✅ |

Unsupported file types will be rejected with a 400 response.

---

## 🧪 Validation and Testing Notes

The repository includes a few validation scripts:

- `model_test.py` checks whether Gemini model names are accessible with the current API key
- `test.py` appears to be a scratch/experimentation file and may not be part of production usage

You can use these to verify connectivity before running the app in a new environment.

---

## 🔒 Notes and Best Practices

- Keep your `.env` file private and never commit secrets.
- Do not expose the app publicly without authenticating access if run in a shared environment.
- Uploaded documents are indexed in Chroma and stored under `uploads/` and `chroma_db/`.
- Thread-specific memory is stored in SQLite and is not globally shared across all users unless you deliberately extend the system.

---

## 🚀 Recommended Use Cases

- Internal knowledge assistant for uploaded PDFs and notes
- Customer support assistant with document grounding
- Personal AI workspace for chats, memory, and file lookup
- Research assistant with web search + document analysis

---

## 🏁 Summary

Orvyn is a practical AI chat application that blends:

- LLM chat
- vector-based document RAG
- live web search
- memory tools
- conversation history
- a clean local web interface

It is a strong example of a lightweight, full-stack agent application built with Python and modern LangChain tooling.

---

<div align="center">

🚀 Built with passion for intelligent, document-aware AI

</div>
