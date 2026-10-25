import requests
import json

print("\n=== ТЕСТ УМНОГО ROUTER С КАРАКАЛПАКСКИМ ===\n")

# Тест на каракалпакском
print("Тест: Каракалпакский язык")
print("-" * 60)

payload = {
    "type": "text",
    "content": "Сәлем! Қалайсыз? Мен билим алғым келеди.",
    "language": "karakalpak",
    "max_tokens": 200
}

try:
    response = requests.post(
        "http://localhost:3000/api/v1/process",
        json=payload,
        timeout=45
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Статус: {result['status']}")
        print(f"✓ Язык: {result['language']}")
        print(f"\n📝 Ваш текст:")
        print(f"   {result['input_text']}")
        print(f"\n✍️ После Styler:")
        print(f"   {result['processed_text']}")
        print(f"\n🤖 Ответ AI на каракалпакском:")
        print(f"   {result['response']}")
        print()
    else:
        print(f"✗ Ошибка: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"✗ Ошибка: {e}")

print("=" * 60)
