from pydantic import BaseModel, Field
from typing import List, Optional

class ContextualBankCardExtraction(BaseModel):
    """
    Номера банковских карт с учетом контекста диалога, переспросов и уточнений.
    
    КОНТЕКСТНЫЕ МАРКЕРЫ:
    - "карта", "номер карты", "банковская карта", "платежная карта"
    - Переспросы: "Погодите, четыре пять шесть семь?", "А дальше?"
    - Повторы и уточнения между оператором и клиентом
    
    ПРИМЕРЫ:
    - "Номер карты: четыре пять шесть семь восемь девять ноль один два три четыре пять шесть семь восемь"
    - "Оператор: Погодите, четыре пять шесть семь? Клиент: Да, четыре пять шесть семь восемь девять ноль один два три четыре пять шесть семь восемь"
    """
    contextual_markers: List[str] = Field(default_factory=list, description="Маркеры контекста: 'карта', 'номер карты', 'банковская карта'")
    raw_fragments: List[str] = Field(default_factory=list, description="Фрагменты номера карты: 'четыре пять шесть семь', 'восемь девять ноль один'")
    reconstructed_card: Optional[str] = Field(None, description="Собранный номер карты: '4567 8901 2345 6789'")
    is_valid: bool = Field(default=False, description="Является ли reconstructed_card валидным номером карты?")
    dialog_context: str = Field(default="", description="Контекст диалога: кто диктует, есть ли переспросы")
    justification: str = Field(default="", description="Объясни: 1) Какие контекстные маркеры найдены, 2) Какие фрагменты номера карты, 3) Почему это один номер карты")
    fragments_to_replace: List[str] = Field(default_factory=list, description="ВСЕ фрагменты для замены: маркеры + номер карты")







