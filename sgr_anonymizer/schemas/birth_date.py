from pydantic import BaseModel, Field
from typing import List

class BirthDateExtraction(BaseModel):
    """
    Дата рождения: '01.01.1990', '1 января 1990 г.'
    """
    raw_dates: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему дата рождения — ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)