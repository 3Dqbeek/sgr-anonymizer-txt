from pydantic import BaseModel, Field
from typing import List

class SnilsExtraction(BaseModel):
    """
    СНИЛС: '123-456-789 01', '12345678901'
    """
    raw_snils: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему СНИЛС — ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)