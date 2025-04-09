import os
import re
from pathlib import Path

def chunk_text(text, max_words=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = words[i:i + max_words]
        chunks.append(" ".join(chunk))
        i += max_words - overlap

    return chunks

def load_scraped_data(file_path="scraped_output.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Split by URL sections
    sections = re.split(r'--- (https?://[^\s]+) ---', raw_text)
    chunks_by_url = {}

    for i in range(1, len(sections), 2):
        url = sections[i].strip()
        text = sections[i+1].strip()
        chunks_by_url[url] = chunk_text(text)

    return chunks_by_url

if __name__ == "__main__":
    chunks_by_url = load_scraped_data()
    output_dir = Path("chunks")
    output_dir.mkdir(exist_ok=True)

    for url, chunks in chunks_by_url.items():
        file_name = re.sub(r'[^\w\-]', '_', url)[:80]  # Safe filename
        with open(output_dir / f"{file_name}.txt", "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(chunk + "\n\n")
