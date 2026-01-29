from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    learner_answer: str
    


class ToneScore(BaseModel):
    score: int
    detected: str
    feedback: str
    improvement: str


class ArticulationScore(BaseModel):
    score: int
    feedback: str
    improvement: str


class EmotionScore(BaseModel):
    score: int
    detected: list[str]
    feedback: str
    improvement: str


class PaceScore(BaseModel):
    score: int
    feedback: str
    improvement: str


class AccuracyScore(BaseModel):
    score: int
    feedback: str
    improvement: str


class OverallFeedback(BaseModel):
    feedback: str
    coachingSuggestions: list[str]


class EvaluationResponse(BaseModel):
    tone: ToneScore
    articulation: ArticulationScore
    emotion: EmotionScore
    pace: PaceScore
    accuracy: AccuracyScore
    overall: OverallFeedback