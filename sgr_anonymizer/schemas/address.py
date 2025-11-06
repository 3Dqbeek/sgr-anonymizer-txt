from pydantic import BaseModel, Field
from typing import List

class AddressExtraction(BaseModel):
    """
    Адреса: 'г. Москва, ул. Тверская, д. 10', '123456, Россия, г. СПб', 'кв. 25'.
    Не включает общие упоминания без идентификации.
    """
    raw_addresses: List[str] = Field(default_factory=list)
    justification: str = Field(default="", description="Почему адрес позволяет идентифицировать лицо? Пример: 'ул. Ленина, д. 10' → ПДн; 'Москва' → не ПДн.")
    fragments_to_replace: List[str] = Field(default_factory=list)