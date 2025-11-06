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
    Сортирует по длине (длинные — первыми), заменяет с экранированием.
    """
    sorted_repl = sorted(replacements, key=lambda x: len(x[0]), reverse=True)
    for frag, tag in sorted_repl:
        if not frag.strip():
            continue
        escaped = re.escape(frag)
        text = re.sub(escaped, f"[{tag}]", text, flags=re.IGNORECASE)
    return text

def regex_safety_net(text: str) -> str:
    """
    Дополнительная страховка: анонимизирует базовые сущности, если что-то пропущено LLM.
    Дублируется здесь для совместимости с импортом пакета utils.
    """
    result = text

    # Email
    email_pattern = r"(?i)(?<!\w)([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})(?!\w)"
    result = re.sub(email_pattern, "[EMAIL]", result, flags=re.IGNORECASE)

    # Телефоны
    phone_patterns = [
        r"(?i)(?<!\d)(\+7|8)?\s*\(?\d{3}\)?[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)",
        r"(?i)(?<!\d)\d{10,12}(?!\d)",
    ]
    for p in phone_patterns:
        result = re.sub(p, "[ТЕЛЕФОН]", result)

    # IP
    ip_pattern = r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"
    result = re.sub(ip_pattern, "[IP-АДРЕС]", result)

    # Паспорт
    passport_pattern = r"(?i)(?:серия\s*)?\b\d{2}\s?\d{2}\b\s*(?:номер\s*)?\b\d{6}\b"
    result = re.sub(passport_pattern, "[ПАСПОРТ]", result)

    # СНИЛС
    snils_pattern = r"(?<!\d)\d{3}-?\d{3}-?\d{3}\s?\d{2}(?!\d)"
    result = re.sub(snils_pattern, "[СНИЛС]", result)

    # ИНН
    inn_pattern = r"(?<!\d)\d{10}(?!\d)|(?<!\d)\d{12}(?!\d)"
    result = re.sub(inn_pattern, "[ИНН]", result)

    # Номер карты
    card_pattern = r"(?<!\d)(?:\d{4}[\s-]?){3}\d{4}(?!\d)"
    result = re.sub(card_pattern, "[НОМЕР КАРТЫ]", result)

    # Дата рождения
    dob_pattern = r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])[\.-](?:0?[1-9]|1[0-2])[\.-](?:19|20)\d{2}(?!\d)"
    result = re.sub(dob_pattern, "[ДАТА РОЖДЕНИЯ]", result)

    return result

def compress_repeated_tags(text: str) -> str:
    """
    Сжимает подряд идущие одинаковые теги в один: [АДРЕС] [АДРЕС] → [АДРЕС].
    """
    tags = [
        'ФИО','ТЕЛЕФОН','EMAIL','АДРЕС','ПАСПОРТ','СНИЛС','ИНН','НОМЕР КАРТЫ',
        'ДАТА РОЖДЕНИЯ','РОДСТВЕННАЯ СВЯЗЬ','IP-АДРЕС'
    ]
    result = text
    for tag in tags:
        # Ищем повторяющиеся теги с пробелами между ними: [TAG] [TAG] [TAG]...
        escaped_tag = re.escape(tag)
        pattern = rf"\[{escaped_tag}\]\s*(?:\[{escaped_tag}\]\s*)+"
        result = re.sub(pattern, f"[{tag}]", result)
    return result