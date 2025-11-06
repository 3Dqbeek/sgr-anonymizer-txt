from pydantic import BaseModel, Field
from typing import List

class BankCardExtraction(BaseModel):
    """
    Номера карт: '4276 1234 5678 9012'
    """
    raw_cards: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему номер карты — ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)