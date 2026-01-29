from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)



def embed_text(text):
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def add_embeddings_to_collection(rag_chunks, collection):
    for chunk in rag_chunks:
        embedding = embed_text(chunk["search_text"])

        collection.add(
            ids=[chunk["chunk_id"]],
            embeddings=[embedding],
            metadatas=[{
                "course_id": chunk["course_id"],
                "event_id": chunk["event_id"],
                "segment_id": chunk["segment_id"]
            }],
            documents=[chunk["search_text"]]
        )
   
