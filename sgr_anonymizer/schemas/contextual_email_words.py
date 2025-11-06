from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualEmailWordsExtraction(BaseModel):
    """
    Email адреса, произнесённые словами с учетом контекста диалога.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "продиктую почту", "диктую email", "электронная почта"
    - "собака", "точка", "ин точка ру", "дот ком"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Давайте продиктую почту: митап четыре три два собака ин точка ру"
    - "Оператор: Погодите, митап? Клиент: Да, митап четыре три два собака ин точка ру"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'продиктую почту', 'email'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты диктовки: 'митап', 'собака', 'ин точка ру'")
    reconstructed_email: Optional[str] = Field(None, description="Собранный email: mitap432@in.ru")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_email валидным email адресом?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, кто записывает, есть ли повторы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты диктовки, 3) Почему это один email")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + диктовка")
