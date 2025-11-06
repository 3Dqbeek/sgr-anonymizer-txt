from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualAddressExtraction(BaseModel):
    """
    Адреса с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "адрес", "живу", "находится", "доставка", "проживаю"
    - Переспросы: "Погодите, Тверская?", "А номер дома какой?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Адрес: Москва, улица Тверская, дом десять"
    - "Оператор: Погодите, Тверская? Клиент: Да, Тверская улица, дом десять"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'адрес', 'живу', 'находится', 'доставка'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты адреса: 'Москва', 'Тверская', 'десять'")
    reconstructed_address: Optional[str] = Field(None, description="Собранный адрес: 'Москва, ул. Тверская, д. 10'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_address валидным адресом?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты адреса, 3) Почему это один адрес")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + адрес")







