from pydantic import BaseModel, Field
from typing import List

class PhoneDigitsExtraction(BaseModel):
    """
    Телефоны цифрами: '+79161234567', '8 (495) 123-45-67', '7-916-123-45-67'
    """
    raw_numbers: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему номер относится к субъекту ПДн?")
    fragments_to_replace: List[str] = Field(default_factory=list)