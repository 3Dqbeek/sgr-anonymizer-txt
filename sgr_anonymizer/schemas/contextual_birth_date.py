from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualBirthDateExtraction(BaseModel):
    """
    Даты рождения с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "дата рождения", "родился", "год рождения", "день рождения"
    - Переспросы: "Погодите, девяносто первый?", "А месяц какой?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Дата рождения: пятнадцатое мая тысяча девятьсот девяносто первого года"
    - "Оператор: Погодите, девяносто первый? Клиент: Да, тысяча девятьсот девяносто первый год"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'дата рождения', 'родился', 'год рождения'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты даты: 'пятнадцатое', 'мая', 'девяносто первый'")
    reconstructed_date: Optional[str] = Field(None, description="Собранная дата: '15.05.1991'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_date валидной датой?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты даты, 3) Почему это одна дата")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + дата")







