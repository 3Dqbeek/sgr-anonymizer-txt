from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualPassportExtraction(BaseModel):
    """
    Паспорта с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "паспорт", "серия", "номер", "документ", "удостоверение"
    - Переспросы: "Погодите, четыре пять шесть семь?", "А номер полностью?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Паспорт: серия четыре пять шесть семь, номер один два три четыре пять шесть"
    - "Оператор: Погодите, четыре пять шесть семь? Клиент: Да, четыре пять шесть семь"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'паспорт', 'серия', 'номер', 'документ'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты паспорта: 'четыре пять шесть семь', 'один два три'")
    reconstructed_passport: Optional[str] = Field(None, description="Собранные данные паспорта: '4567 123456'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_passport валидными данными паспорта?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты паспорта, 3) Почему это один паспорт")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + паспорт")







