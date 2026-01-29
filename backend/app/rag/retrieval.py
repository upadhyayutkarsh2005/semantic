from .vectorstore import collection
from .embeddings import embed_text

def retrieve_context(learner_answer: str, top_k=1 ):
    query_embedding = embed_text(learner_answer)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k ,
    )
    
    return results["ids"][0][0]