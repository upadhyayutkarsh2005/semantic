from fastapi import FastAPI
import json

from app.models import EvaluationRequest, EvaluationResponse
from app.rag.chunker import build_rag_chunks
from app.rag.vectorstore import index_chunks
from app.rag.retrieval import retrieve_context
from app.rag.prompt import build_evaluation_prompt
from app.rag.evaluator import evaluate

app = FastAPI(title="SalesBoost RAG Evaluator")

# 🔥 Load & index data once on startup
with open("data/input.json", "r") as f:
    raw_data = json.load(f)

rag_chunks = build_rag_chunks(raw_data)
index_chunks(rag_chunks)


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_answer(req: EvaluationRequest):
    chunk_id = retrieve_context(
        learner_answer=req.learner_answer,
    )

    context = next(c for c in rag_chunks if c["chunk_id"] == chunk_id)

    prompt = build_evaluation_prompt(context, req.learner_answer)
    result = evaluate(prompt)

    return result

@app.get("/")
def home():
    return {"message": "FastAPI running on Railway"}