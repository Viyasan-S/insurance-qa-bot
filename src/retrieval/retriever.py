
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "chroma_db"
COLLECTION_NAME = "global_life_policy"

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)


def retrieve_policy(question: str, top_k: int = 3) -> list[dict]:
    """Retrieve relevant policy passages for a customer question."""
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance,
        })

    return retrieved


if __name__ == "__main__":
    question = "What is the accidental death benefit?"
    results = retrieve_policy(question)

    print(f"Question: {question}\n")

    for result in results:
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Passage: {result['text']}\n")
