from pydantic import BaseModel, Field
from typing import List

class FIOExtraction(BaseModel):
    """
    ФИО в любых контекстах: разговорный, юридический, медицинский.
    Учитывает полные ФИО, инициалы, обращения, уменьшительно-ласкательные формы.
    """
    candidate_mentions: List[str] = Field(default_factory=list)
    conversational_fio: List[str] = Field(default_factory=list)
    formal_fio: List[str] = Field(default_factory=list)
    ambiguous_mentions: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Объясни для КАЖДОГО упоминания: прямо/косвенно идентифицирует? Примеры: 'Иван Иванович' → ПДн; 'Клиент' → не ПДн.")
    fragments_to_replace: List[str] = Field(default_factory=list)