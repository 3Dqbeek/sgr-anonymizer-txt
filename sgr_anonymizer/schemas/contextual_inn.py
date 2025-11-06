from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualInnExtraction(BaseModel):
    """
    ИНН с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "ИНН", "налоговый номер", "индивидуальный номер", "налоговая"
    - Переспросы: "Погодите, семь семь один?", "А дальше?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "ИНН: семь семь один два три четыре пять шесть семь восемь девять ноль один два"
    - "Оператор: Погодите, семь семь один? Клиент: Да, семь семь один два три четыре пять шесть семь восемь девять ноль один два"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'ИНН', 'налоговый номер', 'индивидуальный номер'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты ИНН: 'семь семь один', 'два три четыре пять'")
    reconstructed_inn: Optional[str] = Field(None, description="Собранный ИНН: '77123456789012'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_inn валидным ИНН?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты ИНН, 3) Почему это один ИНН")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + ИНН")







