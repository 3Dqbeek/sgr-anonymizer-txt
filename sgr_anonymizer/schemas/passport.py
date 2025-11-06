from pydantic import BaseModel, Field
from typing import List

class PassportExtraction(BaseModel):
    """
    Паспорт: '45 12 123456', 'серия 4512 №123456'
    """
    raw_passport: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему паспортные данные — ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)