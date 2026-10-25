import requests
import json
import time

BASE_URL = "http://localhost:3000"

def test_health_checks():
    """Test 1: Check all services are responding"""
    print("\n" + "="*60)
    print("TEST 1: Health Check - All Services")
    print("="*60)

    services = [
        ("Router", "http://localhost:3000/health"),
        ("Ear", "http://localhost:8001/health"),
        ("Brain", "http://localhost:8002/health"),
        ("Styler", "http://localhost:8003/health"),
        ("Voice", "http://localhost:8004/health")
    ]

    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {name:10} - OK - {response.json()}")
            else:
                print(f"✗ {name:10} - FAIL - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ {name:10} - ERROR - {str(e)}")

def test_general_language():
    """Test 2: General language (Russian) processing - direct to Brain"""
    print("\n" + "="*60)
    print("TEST 2: General Language Processing (Russian)")
    print("="*60)

    payload = {
        "type": "text",
        "content": "Что такое искусственный интеллект?",
        "language": "ru"
    }

    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/v1/process", json=payload, timeout=30)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Request successful")
            print(f"  Language detected: {result.get('language')}")
            print(f"  Input: {result.get('input_text')[:50]}...")
            print(f"  Response: {result.get('response')[:100]}...")
            print(f"  Processing time: {elapsed:.2f}s")
        else:
            print(f"✗ Request failed - Status: {response.status_code}")
            print(f"  Error: {response.text}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_karakalpak_language():
    """Test 3: Karakalpak language processing - through full pipeline"""
    print("\n" + "="*60)
    print("TEST 3: Karakalpak Language Processing")
    print("="*60)

    payload = {
        "type": "text",
        "content": "Сәлем, қалайсыз? Мен сизге көмек етейин.",
        "language": "karakalpak"
    }

    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/v1/process", json=payload, timeout=30)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Request successful")
            print(f"  Language detected: {result.get('language')}")
            print(f"  Input: {result.get('input_text')[:50]}...")
            print(f"  Styled: {result.get('processed_text')[:50]}...")
            print(f"  Response: {result.get('response')[:100]}...")
            print(f"  Processing time: {elapsed:.2f}s")
        else:
            print(f"✗ Request failed - Status: {response.status_code}")
            print(f"  Error: {response.text}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_auto_language_detection():
    """Test 4: Auto language detection"""
    print("\n" + "="*60)
    print("TEST 4: Automatic Language Detection")
    print("="*60)

    test_texts = [
        ("English", "Hello, how are you?"),
        ("Russian", "Привет, как дела?"),
        ("Karakalpak", "Бул қандай жұмыс істейді?")
    ]

    for expected_lang, text in test_texts:
        payload = {
            "type": "text",
            "content": text,
            "language": "auto"
        }

        try:
            response = requests.post(f"{BASE_URL}/api/v1/process", json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                detected = result.get('language')
                print(f"  {expected_lang:12} - Detected: {detected:12} - ✓")
            else:
                print(f"  {expected_lang:12} - FAIL")
        except Exception as e:
            print(f"  {expected_lang:12} - ERROR: {str(e)}")

def test_load_stress():
    """Test 5: Load testing with concurrent requests"""
    print("\n" + "="*60)
    print("TEST 5: Load Testing (5 concurrent requests)")
    print("="*60)

    payloads = [
        {"type": "text", "content": f"Тестовый запрос номер {i}", "language": "ru"}
        for i in range(5)
    ]

    start_time = time.time()
    results = []

    for i, payload in enumerate(payloads):
        try:
            response = requests.post(f"{BASE_URL}/api/v1/process", json=payload, timeout=30)
            results.append(response.status_code == 200)
            print(f"  Request {i+1}/5 - {'✓' if response.status_code == 200 else '✗'}")
        except Exception as e:
            results.append(False)
            print(f"  Request {i+1}/5 - ✗ Error: {str(e)}")

    elapsed = time.time() - start_time
    success_rate = (sum(results) / len(results)) * 100

    print(f"\n  Total time: {elapsed:.2f}s")
    print(f"  Success rate: {success_rate:.0f}%")
    print(f"  Average per request: {elapsed/len(payloads):.2f}s")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" TUMARIS AI CLUSTER - TEST SUITE")
    print("="*60)

    time.sleep(1)

    test_health_checks()
    time.sleep(1)

    test_general_language()
    time.sleep(1)

    test_karakalpak_language()
    time.sleep(1)

    test_auto_language_detection()
    time.sleep(1)

    test_load_stress()

    print("\n" + "="*60)
    print(" TEST SUITE COMPLETED")
    print("="*60)
