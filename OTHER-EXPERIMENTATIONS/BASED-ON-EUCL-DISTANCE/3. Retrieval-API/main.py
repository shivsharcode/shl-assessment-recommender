import json
import faiss
import numpy as np
from fastapi import FastAPI, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware

# Load model, index, metadata
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("shl_index.faiss")

with open("shl_index_metadata.json", "r") as f:
    assessments = json.load(f)
    

# FastAPI setup
app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10
    
@app.get('/')
def read_root():
    return {"msg" : "SHL Assessment Recommedation API is running!"}

@app.post('/recommend')
def recommend(req: QueryRequest):
    query_embedding = model.encode([req.query])
    distances, indices = index.search(np.array(query_embedding), req.top_k)
    
    results = []
    for i, ind in enumerate(indices[0]):
        results.append({
            "name": assessments[ind]['name'],
            "url": assessments[ind]['url'],
            'remote_testing': assessments[ind]['remote_testing'],
            "adaptive_testing": assessments[ind]['adaptive_testing'],
            "test_types": assessments[ind]['test_types'],
            "score": float(distances[0][i]),
        })
        
    return {"results": results}