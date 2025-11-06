from pydantic import BaseModel, Field
from typing import List

class InnExtraction(BaseModel):
    """
    ИНН: '770123456789'
    """
    raw_inn: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему ИНН — ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)