#!/usr/bin/env python3
"""
Tumaris AI Cluster - Interactive Client
Интерактивный клиент для тестирования кластера
"""

import requests
import json
import time
import sys
from pathlib import Path

BASE_URL = "http://localhost:3000"
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'red': '\033[91m',
    'cyan': '\033[96m'
}

def print_header():
    print(f"\n{COLORS['cyan']}{'='*60}")
    print("  TUMARIS AI CLUSTER - Interactive Client")
    print(f"{'='*60}{COLORS['reset']}\n")

def print_section(title):
    print(f"\n{COLORS['bold']}{COLORS['blue']}[{title}]{COLORS['reset']}")

def check_cluster_status():
    """Check if all services are running"""
    print_section("Checking Cluster Status")

    services = [
        ("Router", "http://localhost:3000/health"),
        ("Ear", "http://localhost:8001/health"),
        ("Brain", "http://localhost:8002/health"),
        ("Styler", "http://localhost:8003/health"),
        ("Voice", "http://localhost:8004/health")
    ]

    all_ok = True
    for name, url in services:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"  {COLORS['green']}✓{COLORS['reset']} {name:10} - Online")
            else:
                print(f"  {COLORS['red']}✗{COLORS['reset']} {name:10} - Error")
                all_ok = False
        except:
            print(f"  {COLORS['red']}✗{COLORS['reset']} {name:10} - Offline")
            all_ok = False

    return all_ok

def send_text_request(text, language="auto", synthesize=False):
    """Send text processing request"""
    print_section("Processing Request")

    payload = {
        "type": "text",
        "content": text,
        "language": language,
        "synthesize_speech": synthesize
    }

    print(f"  Input: {COLORS['yellow']}{text}{COLORS['reset']}")
    print(f"  Language: {language}")
    print(f"  Synthesize speech: {synthesize}")
    print(f"\n  {COLORS['cyan']}Sending to cluster...{COLORS['reset']}")

    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/v1/process", json=payload, timeout=60)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()

            print(f"\n  {COLORS['green']}✓ Success{COLORS['reset']}")
            print(f"  Processing time: {elapsed:.2f}s")
            print(f"\n  {COLORS['bold']}Detected Language:{COLORS['reset']} {result.get('language')}")

            if result.get('processed_text') != result.get('input_text'):
                print(f"  {COLORS['bold']}Styled Text:{COLORS['reset']} {result.get('processed_text')}")

            print(f"\n  {COLORS['bold']}Response:{COLORS['reset']}")
            print(f"  {COLORS['green']}{result.get('response')}{COLORS['reset']}")

            if result.get('audio_url'):
                print(f"\n  {COLORS['cyan']}Audio available at:{COLORS['reset']} {result.get('audio_url')}")

            return result
        else:
            print(f"\n  {COLORS['red']}✗ Error: {response.status_code}{COLORS['reset']}")
            print(f"  {response.text}")
            return None

    except Exception as e:
        print(f"\n  {COLORS['red']}✗ Error: {str(e)}{COLORS['reset']}")
        return None

def interactive_mode():
    """Interactive mode for continuous testing"""
    print_header()

    if not check_cluster_status():
        print(f"\n{COLORS['red']}Error: Some services are not available.{COLORS['reset']}")
        print("Please start the cluster with: start_cluster.bat")
        return

    print(f"\n{COLORS['green']}All services are online!{COLORS['reset']}")
    print(f"\n{COLORS['bold']}Commands:{COLORS['reset']}")
    print("  - Type your text to process")
    print("  - /ru <text>  - Force Russian language")
    print("  - /kk <text>  - Force Karakalpak language")
    print("  - /voice <text> - Synthesize speech")
    print("  - /status - Check cluster status")
    print("  - /quit - Exit")

    while True:
        try:
            print(f"\n{COLORS['cyan']}>{COLORS['reset']} ", end='')
            user_input = input().strip()

            if not user_input:
                continue

            if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                print(f"\n{COLORS['yellow']}Goodbye!{COLORS['reset']}\n")
                break

            if user_input.lower() == '/status':
                check_cluster_status()
                continue

            language = "auto"
            synthesize = False
            text = user_input

            if user_input.startswith('/ru '):
                language = "ru"
                text = user_input[4:]
            elif user_input.startswith('/kk '):
                language = "karakalpak"
                text = user_input[4:]
            elif user_input.startswith('/voice '):
                synthesize = True
                text = user_input[7:]

            if text:
                send_text_request(text, language, synthesize)

        except KeyboardInterrupt:
            print(f"\n\n{COLORS['yellow']}Interrupted. Goodbye!{COLORS['reset']}\n")
            break
        except Exception as e:
            print(f"\n{COLORS['red']}Error: {str(e)}{COLORS['reset']}")

def demo_mode():
    """Run demo with predefined examples"""
    print_header()

    if not check_cluster_status():
        print(f"\n{COLORS['red']}Error: Cluster is not fully available.{COLORS['reset']}")
        return

    print(f"\n{COLORS['green']}Running Demo Mode{COLORS['reset']}")

    demos = [
        {
            "name": "Russian Text",
            "text": "Расскажи про машинное обучение",
            "language": "ru"
        },
        {
            "name": "English Text",
            "text": "What is artificial intelligence?",
            "language": "en"
        },
        {
            "name": "Karakalpak Text",
            "text": "Сәлем, қалайсыз? Бул қандай жұмыс?",
            "language": "karakalpak"
        },
        {
            "name": "Auto Detection (Karakalpak)",
            "text": "Мен үйренемін",
            "language": "auto"
        }
    ]

    for i, demo in enumerate(demos, 1):
        print(f"\n{COLORS['bold']}Demo {i}/{len(demos)}: {demo['name']}{COLORS['reset']}")
        send_text_request(demo['text'], demo['language'])

        if i < len(demos):
            print(f"\n{COLORS['yellow']}Waiting 2 seconds...{COLORS['reset']}")
            time.sleep(2)

    print(f"\n{COLORS['green']}Demo completed!{COLORS['reset']}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        interactive_mode()
