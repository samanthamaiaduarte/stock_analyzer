from pydantic import BaseModel, Field
from typing import Literal, List

class AIResponse(BaseModel):
    cot: str = Field(description="Internal chain of thought used to reach the conclusion, detailing all your thought processes and reasoning.")
    ticker: str = Field(description="String representing the stock ticker symbol.")
    action: Literal["buy", "sell", "hold"] = Field(description='One of three possible strings indicating the recommended action (possible values are "buy", "sell", "hold").')
    confidence: float = Field(ge = 0, le = 1, description="A float value between 0 and 1 representing the confidence level of your recommendation.")
    reasoning: str = Field(description="String with a detailed explanation of the factors influencing your recommendation.")
    risks: List[str] = Field(description="List of string with comprehensive potential risks associated with the recommended action and links associated with each risk.")
    opportunities: List[str] = Field(description="List of string with comprehensive potential opportunities associated with the recommended action and links associated with each opportunity.")