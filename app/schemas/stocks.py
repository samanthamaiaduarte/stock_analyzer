from pydantic import BaseModel
from typing import Literal, List

class AIOutput(BaseModel):
    ticker: str
    action: Literal["buy", "sell", "hold"]
    confidence: float
    reasoning: str
    risks: List[str]
    opportunities: List[str]

class AIInput(BaseModel):
    ticker: str