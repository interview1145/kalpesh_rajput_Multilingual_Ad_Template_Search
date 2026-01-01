# 🔍 Multilingual Ad Template Search Engine

A full-stack semantic search application that allows users to find the most relevant ad templates using AI-powered multilingual embeddings.

## 🚀 Features
- **Semantic Search**: Understands intent, not just keywords.
- **Multilingual**: Search in 50+ languages for English templates.
- **Smart Ranking**: Results are ranked by a combination of Semantic Similarity, Recency, and Popularity.
- **Fast Performance**: Uses FAISS for lightning-fast vector retrieval.
- **Modern Tech Stack**: Built with FastAPI, Streamlit, and the `uv` package manager.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **AI Model**: `paraphrase-multilingual-MiniLM-L12-v2` (Sentence-Transformers)
- **Environment**: `uv` (Astral)

## 📂 Project Structure
```text
.
├── data/
│   ├── ad_faiss.index      # Pre-computed vector index
│   ├── ad_ids.npy          # Mapping of index to template IDs
│   └── ad_templates.json   # Full template metadata
├── main.py                 # FastAPI Backend
├── app.py                  # Streamlit Frontend
├── pyproject.toml          # Dependency definitions
└── README.md               # Project documentation

Terminal 1 : uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
Terminal 2 : uv run streamlit run app.py

