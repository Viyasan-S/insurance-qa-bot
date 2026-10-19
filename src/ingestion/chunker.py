
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 120,
    overlap: int = 30,
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping word chunks.
    Preserve page numbers for source citations.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    chunks = []

    for page in pages:
        words = page["text"].split()
        start = 0
        chunk_index = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))

            chunks.append({
                "page": page["page"],
                "chunk": chunk_index,
                "text": " ".join(words[start:end]),
            })

            if end == len(words):
                break

            start = end - overlap
            chunk_index += 1

    return chunks
