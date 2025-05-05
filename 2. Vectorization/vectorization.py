import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# for cosine similarity, normalizing method
from sklearn.preprocessing import normalize

# Load the scraped data
with open("shl_assessments_complete.json", "r")as f:
    assessments = json.load(f)
    
# Prepare text data for embedding
texts = []

for a in assessments:
    texts.append(
        f"{a['name']}. {a['description']} "
        f"Test Types: {', '.join(a['test_types'])}."
        f"Remote: {a['remote_support']}, "
        f"Adaptive: {a['adaptive_support']}"
        f"Duration: {a['duration']} minutes."
    )
    
# Load sentence transformer model
model = SentenceTransformer("all-mpnet-base-v2") # Mean Recall@3: 0.098 , Mean MAP@3: 0.222 

# Generate vectorized embeddings of the individual assessments data
embedding = model.encode(texts, show_progress_bar=True)

# Normalize embeddings to unit length (cosine)
embedding = normalize(embedding)

# Store this embeddings in FAISS index
dimension = embedding.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(np.array(embedding))

# Save the index and metadata
faiss.write_index(index, "shl_index.faiss")

with open("shl_index_metadata.json", "w") as f:
    json.dump(assessments, f, indent=2)
    

print(f"✅ Cosine-based FAISS index created for {len(assessments)} assessments.")