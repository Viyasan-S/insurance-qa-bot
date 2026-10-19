
from pathlib import Path
import hashlib

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_pages

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "chroma_db"
COLLECTION_NAME = "global_life_policy"


def main():
    pages = load_pdf()
    chunks = chunk_pages(pages)

    if not chunks:
        raise ValueError("No text was extracted from the policy PDF")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    ids = []
    documents = []
    metadatas = []

    for item in chunks:
        text = item["text"]
        page = item["page"]
        chunk_index = item["chunk"]

        unique_id = hashlib.sha256(
            f"{page}:{chunk_index}:{text}".encode("utf-8")
        ).hexdigest()[:24]

        ids.append(unique_id)
        documents.append(text)
        metadatas.append({
            "source": "mock_life_insurance_policy.pdf",
            "page": page,
            "chunk": chunk_index,
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print("Policy indexed successfully!")
    print(f"Pages processed: {len(pages)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Total chunks in collection: {collection.count()}")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    main()
