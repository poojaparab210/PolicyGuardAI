
import re


def clean_text(text: str) -> str:
    """Clean extracted policy text while preserving its meaning."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[str]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size.")

    words = clean_text(text).split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks


def extract_keywords(text: str) -> list[str]:
    """Extract a small set of frequent meaningful words."""
    stop_words = {
        "the", "and", "for", "with", "this", "that", "from",
        "are", "was", "were", "will", "should", "may", "can",
        "into", "their", "they", "you", "your", "have", "has",
    }

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return sorted({
        word for word in words if word not in stop_words
    })
