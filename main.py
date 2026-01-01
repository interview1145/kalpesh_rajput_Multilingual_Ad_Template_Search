
from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone
import math

DATA_PATH = Path("data")

app = FastAPI(title="Ad Search API")

# --- DATA LOADING ---
try:
    index = faiss.read_index(str(DATA_PATH / "ad_faiss.index"))
    ids = np.load(DATA_PATH / "ad_ids.npy")
    with open(DATA_PATH / "ad_templates.json", "r", encoding="utf-8") as f:
        templates_list = json.load(f)
    templates = {tpl["id"]: tpl for tpl in templates_list}
    print(f"✅ Loaded {index.ntotal} templates")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    raise

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
NOW = datetime.now(timezone.utc)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResponse(BaseModel):
    results: list
    total_found: int

def ranking_score(similarity, created_at, usage_count):
    try:
        created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        if created.tzinfo is None: created = created.replace(tzinfo=timezone.utc)
        age_days = max((NOW - created).days + 1, 1)
        recency = 1.0 / math.log1p(age_days)
        popularity = math.log1p(usage_count)
        return (0.6 * similarity) + (0.25 * recency) + (0.15 * popularity)
    except: return similarity

@app.get("/")
def home():
    return {"status": "online", "docs": "/docs"}

@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    q_vec = model.encode([req.query], normalize_embeddings=True)
    scores, indices = index.search(q_vec, req.top_k * 3)
    
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1: continue
        tpl = templates.get(int(ids[idx]))
        if not tpl: continue
        
        results.append({
            "id": int(ids[idx]),
            "sim_score": float(score),
            "rank_score": ranking_score(float(score), tpl["created_at"], tpl["usage_count"]),
            "title": tpl["title"],
            "description": tpl["description"],
            "category": tpl["category"],
            "created_at": tpl["created_at"],
            "usage_count": tpl["usage_count"],
        })
    
    results.sort(key=lambda x: x["rank_score"], reverse=True)
    return SearchResponse(results=results[:req.top_k], total_found=len(results))
