# sgr_anonymizer/utils.py
import re
import json

def clean_json_string(s: str) -> str:
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
    s = s.strip()
    if s.startswith("```json"):
        s = s[7:]
    if s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()

def anonymize_with_tags(text: str, replacements: list) -> str:
    """
    replacements: [(fragment, tag), ...]
    Умная замена: заменяет все вхождения каждого фрагмента.
    Сначала заменяет длинные фрагменты, потом короткие (чтобы длинные не мешали коротким).
    """
    if not replacements:
        return text
    
    # Удаляем дубликаты, оставляя последний вариант
    unique_replacements = {}
    for frag, tag in replacements:
        if frag.strip():
            # Используем оригинальный фрагмент как ключ для сохранения регистра
            key = frag.lower()
            if key not in unique_replacements or len(frag) > len(unique_replacements[key][0]):
                unique_replacements[key] = (frag, tag)
    
    # Сортируем по длине (длинные первыми)
    sorted_repl = sorted(unique_replacements.values(), key=lambda x: len(x[0]), reverse=True)
    
    result_text = text
    
    # Заменяем каждый фрагмент по очереди (сначала длинные, потом короткие)
    for frag, tag in sorted_repl:
        escaped = re.escape(frag)
        # Заменяем все вхождения фрагмента
        result_text = re.sub(escaped, f"[{tag}]", result_text, flags=re.IGNORECASE)
    
    return result_text

def regex_safety_net(text: str) -> str:
    """
    Дополнительная страховка: анонимизирует базовые сущности, если что-то пропущено LLM.
    Предназначено для снижения вероятности утечек при редких сбоях парсинга JSON.
    """
    result = text

    # Email (включая простые варианты)
    email_pattern = r"(?i)(?<!\w)([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})(?!\w)"
    result = re.sub(email_pattern, "[EMAIL]", result, flags=re.IGNORECASE)

    # Телефоны цифрами (российские форматы + общие варианты длиной 10-12)
    phone_patterns = [
        r"(?i)(?<!\d)(\+7|8)?\s*\(?\d{3}\)?[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)",
        r"(?i)(?<!\d)\d{10,12}(?!\d)",
    ]
    for p in phone_patterns:
        result = re.sub(p, "[ТЕЛЕФОН]", result)

    # IP-адреса
    ip_pattern = r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"
    result = re.sub(ip_pattern, "[IP-АДРЕС]", result)

    # Номер паспорта РФ: серия 4 цифры и номер 6 цифр (вольно)
    passport_pattern = r"(?i)(?:серия\s*)?\b\d{2}\s?\d{2}\b\s*(?:номер\s*)?\b\d{6}\b"
    result = re.sub(passport_pattern, "[ПАСПОРТ]", result)

    # СНИЛС: 3-3-3-2 цифры
    snils_pattern = r"(?<!\d)\d{3}-?\d{3}-?\d{3}\s?\d{2}(?!\d)"
    result = re.sub(snils_pattern, "[СНИЛС]", result)

    # ИНН: 10 или 12 цифр (отличая от телефонов по контексту сложно, но подстрахуемся)
    inn_pattern = r"(?<!\d)\d{10}(?!\d)|(?<!\d)\d{12}(?!\d)"
    result = re.sub(inn_pattern, "[ИНН]", result)
    
    # Номер карты: 16 цифр с пробелами или без
    card_pattern = r"(?<!\d)(?:\d{4}[\s-]?){3}\d{4}(?!\d)"
    result = re.sub(card_pattern, "[НОМЕР КАРТЫ]", result)

    # Дата рождения: простые форматы dd.mm.yyyy, dd-mm-yyyy
    dob_pattern = r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])[\.-](?:0?[1-9]|1[0-2])[\.-](?:19|20)\d{2}(?!\d)"
    result = re.sub(dob_pattern, "[ДАТА РОЖДЕНИЯ]", result)

    return result

def compress_repeated_tags(text: str) -> str:
    """
    Сжимает подряд идущие одинаковые теги в один: [АДРЕС] [АДРЕС] → [АДРЕС].
    Работает для всех известных тегов.
    """
    tags = [
        'ФИО','ТЕЛЕФОН','EMAIL','АДРЕС','ПАСПОРТ','СНИЛС','ИНН','НОМЕР КАРТЫ',
        'ДАТА РОЖДЕНИЯ','РОДСТВЕННАЯ СВЯЗЬ','IP-АДРЕС'
    ]
    result = text
    for tag in tags:
        pattern = rf"(?:\[{re.escape(tag)}\])(\s*(?:\[{re.escape(tag)}\]))+"
        result = re.sub(pattern, f"[{tag}]", result)
    return result