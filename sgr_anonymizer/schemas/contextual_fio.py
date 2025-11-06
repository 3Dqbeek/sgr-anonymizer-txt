from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualFIOExtraction(BaseModel):
    """
    ФИО с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "зовут", "фамилия", "имя", "отчество", "меня зовут"
    - Переспросы: "Погодите, Иванов?", "А отчество как?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Меня зовут Иванов Иван Иванович"
    - "Оператор: Погодите, Иванов? Клиент: Да, Иванов Иван Иванович"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'зовут', 'фамилия', 'имя', 'отчество'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты ФИО: 'Иванов', 'Иван', 'Иванович'")
    reconstructed_fio: Optional[str] = Field(None, description="Собранное ФИО: 'Иванов Иван Иванович'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_fio валидным ФИО?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты ФИО, 3) Почему это одно ФИО")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + ФИО")







