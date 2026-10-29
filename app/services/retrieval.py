
import chromadb
from sentence_transformers import SentenceTransformer

from app.services.nlp_processor import split_into_chunks


# Load the embedding model once when this module is imported.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Persist the vector database locally.
client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(
    name="policyguard_chunks",
    metadata={"hnsw:space": "cosine"},
)


def index_policy(policy_id: str, text: str) -> int:
    """Split a policy into chunks and store its embeddings."""
    chunks = split_into_chunks(text, chunk_size=180, overlap=30)

    if not chunks:
        return 0

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True,
    ).tolist()

    ids = [f"{policy_id}_{i}" for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"policy_id": policy_id, "chunk_index": i}
            for i in range(len(chunks))
        ],
    )

    return len(chunks)


def search_policy(
    policy_id: str,
    question: str,
    top_k: int = 3,
) -> list[dict]:
    """Retrieve the most relevant chunks from one policy."""
    if not question.strip():
        return []

    result = collection.query(
        query_embeddings=[
            embedding_model.encode(
                question,
                normalize_embeddings=True,
            ).tolist()
        ],
        n_results=top_k,
        where={"policy_id": policy_id},
        include=["documents", "metadatas", "distances"],
    )

    documents = result["documents"][0] if result["documents"] else []
    metadatas = result["metadatas"][0] if result["metadatas"] else []
    distances = result["distances"][0] if result["distances"] else []

    return [
        {
            "text": document,
            "chunk_index": metadata["chunk_index"],
            "distance": distance,
        }
        for document, metadata, distance
        in zip(documents, metadatas, distances)
    ]
