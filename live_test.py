import requests
import json

print("\n=== 🧪 ЖИВОЙ ТЕСТ КЛАСТЕРА TUMARIS ===\n")

# Тест 1: Русский текст
print("Тест 1: Русский текст")
print("-" * 50)

payload = {
    "type": "text",
    "content": "Привет! Расскажи мне про искусственный интеллект кратко",
    "language": "ru",
    "max_tokens": 150
}

try:
    response = requests.post(
        "http://localhost:3000/api/v1/process",
        json=payload,
        timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Статус: {result['status']}")
        print(f"✓ Язык: {result['language']}")
        print(f"✓ Запрос: {result['input_text']}")
        print(f"\n✓ Ответ модели:")
        print(f"  {result['response']}\n")
    else:
        print(f"✗ Ошибка: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"✗ Ошибка: {e}")

# Тест 2: Английский текст
print("\nТест 2: Английский текст")
print("-" * 50)

payload2 = {
    "type": "text",
    "content": "Hello! What is machine learning?",
    "language": "en",
    "max_tokens": 100
}

try:
    response2 = requests.post(
        "http://localhost:3000/api/v1/process",
        json=payload2,
        timeout=30
    )

    if response2.status_code == 200:
        result2 = response2.json()
        print(f"✓ Статус: {result2['status']}")
        print(f"✓ Язык: {result2['language']}")
        print(f"✓ Запрос: {result2['input_text']}")
        print(f"\n✓ Ответ модели:")
        print(f"  {result2['response']}\n")
    else:
        print(f"✗ Ошибка: {response2.status_code}")

except Exception as e:
    print(f"✗ Ошибка: {e}")

print("\n" + "="*50)
print("✅ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("="*50 + "\n")
