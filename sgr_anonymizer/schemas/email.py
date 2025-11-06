from pydantic import BaseModel, Field
from typing import List

class EmailExtraction(BaseModel):
    """
    Email: 'user@example.com', 'ivan.petrov@mail.ru'
    """
    raw_emails: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему email — ПДн по ФЗ-152?")
    fragments_to_replace: List[str] = Field(default_factory=list)