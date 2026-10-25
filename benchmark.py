"""
Performance benchmarking script for Tumaris cluster
"""

import requests
import time
import statistics

BASE_URL = "http://localhost:3000"

def benchmark_latency(endpoint, payload, iterations=5):
    """Measure average latency"""
    latencies = []

    print(f"\nBenchmarking {endpoint} ({iterations} iterations)...")

    for i in range(iterations):
        start = time.time()
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=60)
            elapsed = time.time() - start

            if response.status_code == 200:
                latencies.append(elapsed)
                print(f"  Iteration {i+1}: {elapsed:.3f}s ✓")
            else:
                print(f"  Iteration {i+1}: Failed ✗")
        except Exception as e:
            print(f"  Iteration {i+1}: Error - {e}")

    if latencies:
        avg = statistics.mean(latencies)
        med = statistics.median(latencies)
        std = statistics.stdev(latencies) if len(latencies) > 1 else 0

        print(f"\n  Results:")
        print(f"    Average: {avg:.3f}s")
        print(f"    Median:  {med:.3f}s")
        print(f"    Std Dev: {std:.3f}s")
        print(f"    Min:     {min(latencies):.3f}s")
        print(f"    Max:     {max(latencies):.3f}s")

        return avg
    else:
        print(f"\n  All requests failed!")
        return None

def main():
    print("="*60)
    print(" TUMARIS PERFORMANCE BENCHMARK")
    print("="*60)

    benchmarks = [
        {
            "name": "General Language (Russian)",
            "endpoint": "/api/v1/process",
            "payload": {
                "type": "text",
                "content": "Расскажи про машинное обучение",
                "language": "ru",
                "max_tokens": 256
            }
        },
        {
            "name": "Karakalpak Language",
            "endpoint": "/api/v1/process",
            "payload": {
                "type": "text",
                "content": "Сәлем, мен сизге көмек етейин",
                "language": "karakalpak",
                "max_tokens": 256
            }
        },
        {
            "name": "Short Generation",
            "endpoint": "/api/v1/process",
            "payload": {
                "type": "text",
                "content": "Hello",
                "language": "en",
                "max_tokens": 128
            }
        }
    ]

    results = {}

    for bench in benchmarks:
        print(f"\n{'='*60}")
        print(f" {bench['name']}")
        print(f"{'='*60}")

        avg_latency = benchmark_latency(
            bench['endpoint'],
            bench['payload'],
            iterations=3
        )

        results[bench['name']] = avg_latency

    print(f"\n{'='*60}")
    print(" SUMMARY")
    print(f"{'='*60}\n")

    for name, latency in results.items():
        if latency:
            print(f"  {name:35} {latency:.3f}s")
        else:
            print(f"  {name:35} FAILED")

    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
