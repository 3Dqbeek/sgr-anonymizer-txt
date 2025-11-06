from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualPhoneWordsExtraction(BaseModel):
    """
    Телефоны, произнесённые словами с учетом контекста диалога.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "продиктую телефон", "диктую номер", "номер телефона"
    - "восемь девять два", "плюс семь", "семьсот один"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Давайте я продиктую телефон: восемь девять два ноль пять восемь"
    - "Оператор: Погодите, восемь девять два? Клиент: Да, восемь девять два ноль пять"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'продиктую телефон', 'номер телефона'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты диктовки: 'восемь девять два', 'плюс семь'")
    reconstructed_number: Optional[str] = Field(None, description="Собранный номер в формате +7XXXXXXXXXX")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_number валидным 11-значным номером РФ?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, кто записывает, есть ли повторы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты диктовки, 3) Почему это один номер")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + диктовка")
