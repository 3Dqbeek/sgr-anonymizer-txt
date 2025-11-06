# llm_client.py
import requests
import os
from dotenv import load_dotenv
#
load_dotenv()

class LLMClient:
    """
    Клиент для работы с LLM через LM Studio (или другой OpenAI-совместимый API).
    Используется ТОЛЬКО для генерации текста (классификация, анализ, переформулировка),
    НЕ для эмбеддингов.
    """
    
    def __init__(self):
        self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://192.168.1.9:1234")
        self.model = os.getenv("CLASSIFICATION_MODEL1", "qwen/qwen3-coder-30b")

        # Проверка подключения к серверу
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=100)
            if response.status_code != 200:
                raise ConnectionError(f"Server responded with status {response.status_code}")
            
            data = response.json()
            available_models = [m.get("id") for m in data.get("data", [])]
            
            if self.model not in available_models:
                raise ValueError(
                    f"Model '{self.model}' not found. Available models: {available_models}"
                )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"❌ Не удалось подключиться к LM Studio по адресу: {self.base_url}\n"
                "Убедитесь, что LM Studio запущен и API включён на порту 1234."
            )
        except Exception as e:
            raise RuntimeError(f"❌ Ошибка при инициализации LLMClient: {e}")

    def chat_completion(self, messages, temperature=0.0, max_tokens=46683):
        """
        Отправляет запрос к LLM и возвращает сгенерированный текст.
        
        :param messages: список словарей с ключами 'role', 'content'
        :param temperature: температура генерации
        :param max_tokens: максимальное число токенов
        :return: строка — ответ модели
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.Timeout:
            raise TimeoutError("❌ Таймаут при запросе к LM Studio (возможно, модель слишком большая)")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"❌ Ошибка HTTP при обращении к LM Studio: {e}")
        except KeyError:
            raise RuntimeError(f"❌ Неверный формат ответа от сервера: {response.text}")

    def generate(self, prompt, **kwargs):
        """
        Упрощённый метод: один запрос по строке.
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, **kwargs)
    
    def clean_json_string(self, s):
        """
        Очищает JSON строку от лишних символов и markdown форматирования.
        """
        import re
        s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
        s = s.strip()
        if s.startswith("```json"):
            s = s[7:]
        if s.startswith("```"):
            s = s[3:]
        if s.endswith("```"):
            s = s[:-3]
        return s.strip()