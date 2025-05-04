import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the scraped data
with open("shl_assessments_paginated.json", "r")as f:
    assessments = json.load(f)
    
# Prepare text data for embedding
texts = []

for a in assessments:
    texts.append(
        f"{a['name']}: Test Types: {', '.join(a['test_types'])}. "
        f"Remote: {'Yes' if a['remote_testing'] else 'No'}, "
        f"Adaptive: {'Yes' if a['adaptive_testing'] else 'No'}"
    )
    
# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate vector embeddings of the individual assessments data
embedding = model.encode(texts, show_progress_bar=True)

# Store this embeddings in FAISS index
dimension = embedding.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embedding))

# Save the index and metadata
faiss.write_index(index, "shl_index.faiss")

with open("shl_index_metadata.json", "w") as f:
    json.dump(assessments, f)
    

print(f"✅ Vector index created for {len(assessments)} assessments.")