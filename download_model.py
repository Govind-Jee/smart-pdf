# In download_model.py
from sentence_transformers import SentenceTransformer

# This downloads the model to a folder so it can be used offline in Docker
# This model is small and fast, perfect for the constraints [cite: 152]
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./sbert-model')
print("✅ Model downloaded to ./sbert-model")