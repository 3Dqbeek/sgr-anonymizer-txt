# SGR Anonymizer для TXT файлов

Приложение для анонимизации персональных данных в текстовых диалогах по ФЗ-152 с использованием SGR методологии.

**Автор:** DautoV Vasiliy  
**Лицензия:** MIT

## Описание

SGR Anonymizer — система автоматической анонимизации персональных данных в текстовых диалогах. Система использует многоуровневую схему извлечения ПДн с применением LLM (Large Language Model) для контекстного анализа и идентификации всех типов персональных данных согласно ФЗ-152.

### Основные возможности

- ✅ Анонимизация 13 типов персональных данных по ФЗ-152
- ✅ Контекстный анализ диалогов с использованием LLM
- ✅ Валидационный цикл для поиска пропущенных сущностей
- ✅ Обработка сложных случаев (телефоны и email словами)
- ✅ Regex safety net для дополнительной защиты
- ✅ Поддержка текстовых диалогов в формате TXT

## Развертывание

### Требования

- Python 3.8+
- Доступ к LLM API (LM Studio или другой совместимый сервис)

### Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/3Dqbeek/sgr-anonymizer-txt.git
cd sgr-anonymizer-txt
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Настройте LLM клиент:

Отредактируйте `llm_client.py` и укажите адрес вашего LLM сервера:

```python
# По умолчанию: http://192.168.1.9:1234/v1/chat/completions
# Измените на адрес вашего LLM сервера
```

### Использование

#### Базовое использование

```bash
python test_random_5_fixed.py
```

Скрипт обработает 5 случайных TXT файлов из директории `dialog_in/` и сохранит результаты в `dialog_test_fixed_random/`.

#### Программное использование

```python
from sgr_anonymizer import SGRFixedAnonymizer

# Создаем анонимизатор
anonymizer = SGRFixedAnonymizer()

# Читаем текст диалога
with open('dialog.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Анонимизируем
anonymized_text = anonymizer.anonymize(text)

# Сохраняем результат
with open('dialog_anonymized.txt', 'w', encoding='utf-8') as f:
    f.write(anonymized_text)
```

## Описание логики работы

### Архитектура обработки

Система использует **многоуровневую схему извлечения** персональных данных с последовательной обработкой 13 типов ПДн:

1. **ФИО** → `[ФИО]`
2. **Телефоны цифрами** → `[ТЕЛЕФОН]`
3. **Телефоны словами** → `[ТЕЛЕФОН]` (контекстная схема)
4. **Email обычные** → `[EMAIL]`
5. **Email словами** → `[EMAIL]` (контекстная схема)
6. **Адреса** → `[АДРЕС]`
7. **Паспорт** → `[ПАСПОРТ]`
8. **СНИЛС** → `[СНИЛС]`
9. **ИНН** → `[ИНН]`
10. **Номер карты** → `[НОМЕР КАРТЫ]`
11. **Дата рождения** → `[ДАТА РОЖДЕНИЯ]`
12. **Родственная связь** → `[РОДСТВЕННАЯ СВЯЗЬ]`
13. **IP-адрес** → `[IP-АДРЕС]`

**Важно:** ФИО обрабатывается первым, чтобы предотвратить ложное определение имен как email или других сущностей.

### Процесс анонимизации

#### Шаг 1: Генерация промпта
Для каждой схемы строится специализированный промпт с:
- Четкими инструкциями по извлечению
- Примерами правильных и неправильных случаев
- Явными исключениями (что НЕ извлекать)
- Указанием игнорировать уже анонимизированные теги

#### Шаг 2: Вызов LLM
- LLM получает промпт и исходный текст
- Возвращает JSON согласно Pydantic-схеме
- При ошибках парсинга JSON — повторная попытка с усиленными инструкциями

#### Шаг 3: Извлечение фрагментов
- Парсинг JSON в Pydantic-модель
- Извлечение списка `fragments_to_replace` (точные цитаты для замены)
- Сбор всех замен в единый список

#### Шаг 4: Умная замена
- Сортировка замен по длине фрагмента (длинные первыми)
- Замена всех вхождений каждого фрагмента на соответствующий тег
- Удаление дубликатов

### Валидационный цикл

Система выполняет **несколько проходов** (до `max_rounds=3`):

```
Текст → Проход 1 → Проход 2 → Проход 3 → Финальный текст
```

**Логика:** Если после прохода текст не изменился → остановка. Иначе — повтор до `max_rounds`.

**Цель:** Найти сущности, которые могли быть пропущены из-за контекстных зависимостей (например, после замены ФИО становится виден телефон).

### Постобработка

#### Regex Safety Net
После валидационного цикла применяются регулярные выражения для "подстраховки":
- Email, телефоны, IP-адреса
- Паспорт, СНИЛС, ИНН, карты, даты рождения

**Цель:** Поймать простые случаи, пропущенные LLM из-за ошибок парсинга JSON.

#### Сжатие повторяющихся тегов
Объединяет подряд идущие одинаковые теги:
- `[АДРЕС] [АДРЕС] [АДРЕС]` → `[АДРЕС]`

### Контекстные схемы

Для обработки сложных случаев (телефоны и email словами) используются контекстные схемы, которые:
1. Ищут маркеры начала диктовки
2. Собирают фрагменты из последовательных реплик
3. Восстанавливают полную сущность из разрозненных частей

## Структура проекта

```
sgr-anonymizer-txt/
├── sgr_anonymizer/          # Основной код анонимизатора
│   ├── core_sgr_fixed.py    # Рабочий модуль анонимизации
│   ├── schemas/              # Pydantic схемы для типов ПДн
│   └── utils.py              # Утилиты
├── test_random_5_fixed.py    # Скрипт для обработки TXT файлов
├── llm_client.py            # Клиент для работы с LLM
├── requirements.txt         # Зависимости
└── README.md               # Документация
```

## Формат входных данных

Диалоги должны быть в текстовом формате с метаданными:

```
[Role]
(start_time - end_time) text
```

Пример:

```
[Customer]
(0.66s - 4.20s) интернет магазин тифа меня зовут мария какой у вас вопрос

[Operator]
(6.09s - 10.92s) здравствуйте вот хотела бы уточнить
```

## Формат выходных данных

После анонимизации персональные данные заменяются на теги:

```
[Customer]
(0.66s - 4.20s) интернет магазин тифа меня зовут [ФИО] какой у вас вопрос
```

## Лицензия

MIT License

Copyright (c) 2025 DautoV Vasiliy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Автор

**DautoV Vasiliy**

## Поддержка

При возникновении проблем создайте Issue в репозитории.
