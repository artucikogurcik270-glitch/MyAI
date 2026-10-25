#!/usr/bin/env python3
"""
Quick test script for Tumaris cluster
Usage: python quick_test.py
"""

import requests
import sys

def quick_test():
    print("\n🔍 Quick Testing Tumaris Cluster...\n")

    # Test 1: Health check
    try:
        r = requests.get("http://localhost:3000/health", timeout=2)
        if r.status_code == 200:
            print("✓ Router is online")
        else:
            print("✗ Router returned error")
            return False
    except:
        print("✗ Router is offline. Run: start_cluster.bat")
        return False

    # Test 2: Simple generation
    try:
        payload = {
            "type": "text",
            "content": "Hello",
            "language": "en"
        }
        r = requests.post("http://localhost:3000/api/v1/process", json=payload, timeout=30)

        if r.status_code == 200:
            result = r.json()
            print(f"✓ Brain is working")
            print(f"  Response: {result.get('response', '')[:80]}...")
        else:
            print(f"✗ Request failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    print("\n✅ Cluster is working correctly!\n")
    return True

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
