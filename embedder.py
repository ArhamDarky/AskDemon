import os
import openai
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set. Use an env variable or .env file.")

# === CONFIG ===
MODEL = "text-embedding-ada-002"
MAX_CHARS = 8000
CHUNK_DIR = "chunks"
OUTPUT_FILE = "embeddings.json"
RATE_LIMIT_DELAY = 0.5  # seconds between requests

def get_embedding(text):
    # Truncate text if too long
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    try:
        response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )

        
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error embedding chunk: {e}")
        return None

def embed_chunks(folder_path=CHUNK_DIR, output_file=OUTPUT_FILE):
    embeddings = []
    chunk_files = list(Path(folder_path).glob("*.txt"))
    total_files = len(chunk_files)
    total_chunks = 0

    print(f"\n🔎 Found {total_files} chunk files in '{CHUNK_DIR}'")

    for file_num, file in enumerate(chunk_files, start=1):
        with open(file, "r", encoding="utf-8") as f:
            chunks = f.read().strip().split("\n\n")

            for chunk_num, chunk in enumerate(chunks, start=1):
                if not chunk.strip():
                    continue

                embedding = get_embedding(chunk)
                if embedding:
                    embeddings.append({
                        "file": str(file),
                        "text": chunk,
                        "embedding": embedding
                    })
                    total_chunks += 1

                time.sleep(RATE_LIMIT_DELAY)

        print(f"✅ Processed {file_num}/{total_files} files")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=2)

    print(f"\n🎉 Done! Saved {total_chunks} chunks to '{output_file}'.")

if __name__ == "__main__":
    embed_chunks()

# This script embeds text chunks from the specified directory and saves them to a JSON file.