import openai
import json
import numpy as np
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_query_embedding(query):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    )
    return response.data[0].embedding

def search(query, embedding_file="embeddings.json", top_k=3):
    query_vec = get_query_embedding(query)

    with open(embedding_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        score = cosine_similarity(query_vec, item["embedding"])
        results.append((score, item["text"]))

    results.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [text for _, text in results[:top_k]]
    return "\n\n".join(top_chunks)

# This function can be called directly to test the search functionality