from pydantic import BaseModel, Field
from typing import List, Optional

class PhoneWordsExtraction(BaseModel):
    """
    Телефоны, произнесённые словами: 'плюс семь', 'семьсот один', 'двадцать три'.
    Учитывает повторы (клиент и оператор), шум, уточнения.
    """
    raw_fragments: List[str] = Field(default_factory=list)
    reconstructed_number: Optional[str] = Field(None, description="Собранный номер в формате +7XXXXXXXXXX")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_number валидным 11-значным номером РФ?")
    justification: str = Field(
        default="",
        description="Объясни:\n"
                    "1. Какие фрагменты использованы (игнорируй повторы и шум)?\n"
                    "2. Почему они относятся к одному номеру?\n"
                    "3. Пример: 'Использованы: плюс семь, семьсот один... Повторы от оператора проигнорированы.'"
    )
    fragments_to_replace: List[str] = Field(default_factory=list)