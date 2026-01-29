from openai import OpenAI
import os
import json

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)

def evaluate(prompt: str) -> dict:
    client = get_openai_client()
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return json.loads(res.choices[0].message.content)
