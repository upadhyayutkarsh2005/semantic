import chromadb
from .embeddings import embed_text

chroma = chromadb.Client()
collection = chroma.get_or_create_collection("sales_rag")


def index_chunks(chunks: list[dict]):
    for chunk in chunks:
        collection.add(
            ids=[chunk["chunk_id"]],
            embeddings=[embed_text(chunk["search_text"])],
            metadatas=[{
                "course_id": chunk["course_id"],
                "event_id": chunk["event_id"],
                "segment_id": chunk["segment_id"]
            }],
            documents=[chunk["search_text"]]
        )