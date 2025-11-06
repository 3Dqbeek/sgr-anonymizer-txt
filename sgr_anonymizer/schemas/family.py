from pydantic import BaseModel, Field
from typing import List

class FamilyExtraction(BaseModel):
    """
    Родственные связи: 'муж', 'жена', 'брат', 'сестра', 'мама', 'папа', 'сын', 'дочь', 'тёща', 'свекр'.
    Только если они относятся к субъекту ПДн.
    """
    raw_relations: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему связь относится к субъекту ПДн? Пример: 'мой муж' → ПДн; 'брат друга' → не ПДн.")
    fragments_to_replace: List[str] = Field(default_factory=list)