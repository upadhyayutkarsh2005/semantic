def build_evaluation_prompt(context, learner_answer):
    return f"""
You are an expert speech and communication coach analyzing a customer service training response.

SCENARIO:
{context['scenario_title']}

Customer emotion:
{context['emotion']}

Customer said:
\"{context['customer_utterance']}\"

EXPECTED RESPONSE (ideal answer):
\"{context['expected_response']}\"

ACTUAL TRANSCRIPTION (learner answer):
\"{learner_answer}\"

IDEAL TONE:
{context.get('ideal_tone', 'Professional and empathetic')}

KEY EMOTIONS TO CONVEY:
{', '.join(context.get('key_emotions', ['Empathy', 'Confidence', 'Warmth']))}

EVALUATION GOAL:
Compare the learner answer with the expected response and evaluate speech quality, emotional delivery, tone, pacing, and script accuracy.

CRITICAL SCORING RULES:
- Use a 0–100 scoring scale.
- Be highly discriminative. Avoid similar scores across categories.
- Scores must reflect actual performance differences.
- Do NOT inflate scores.
- Use concrete observations (word choice, clarity, missing intent, emotional cues).

Return ONLY a valid JSON object in the following EXACT format:

{{
  "tone": {{
    "score": "0-100",
    "detected": "",
    "feedback": "",
    "improvement": ""
  }},
  "articulation": {{
    "score": "0-100",
    "feedback": "",
    "improvement": ""
  }},
  "emotion": {{
    "score": "0-100",
    "detected": [],
    "feedback": "",
    "improvement": ""
  }},
  "pace": {{
    "score": "0-100",
    "feedback": "",
    "improvement": ""
  }},
  "accuracy": {{
    "score": "0-100",
    "feedback": "",
    "improvement": ""
  }},
  "overall": {{
    "feedback": "",
    "coachingSuggestions": []
  }}
}}

IMPORTANT:
- Each score must be meaningfully different (10–30+ point gaps where justified).
- Feedback must be specific and actionable.
- Do not add any text outside the JSON.
"""