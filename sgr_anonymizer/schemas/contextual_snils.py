from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualSnilsExtraction(BaseModel):
    """
    СНИЛС с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "СНИЛС", "страховой номер", "пенсионный", "страховка"
    - Переспросы: "Погодите, сто двадцать три?", "А дальше?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "СНИЛС: сто двадцать три четыре пять шесть семь восемь девять ноль один"
    - "Оператор: Погодите, сто двадцать три? Клиент: Да, сто двадцать три четыре пять шесть семь восемь девять ноль один"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'СНИЛС', 'страховой номер', 'пенсионный'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты СНИЛС: 'сто двадцать три', 'четыре пять шесть семь'")
    reconstructed_snils: Optional[str] = Field(None, description="Собранный СНИЛС: '123-456-789-01'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_snils валидным СНИЛС?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты СНИЛС, 3) Почему это один СНИЛС")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + СНИЛС")







