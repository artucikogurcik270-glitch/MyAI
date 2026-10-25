#!/usr/bin/env python3
"""
Log aggregator for Tumaris cluster
Collects logs from all services
"""

import os
import datetime
from pathlib import Path

def create_log_report():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"D:\\Project\\logs\\cluster_report_{timestamp}.txt"

    os.makedirs("D:\\Project\\logs", exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(" TUMARIS CLUSTER LOG REPORT\n")
        f.write(f" Generated: {datetime.datetime.now()}\n")
        f.write("="*70 + "\n\n")

        # System info
        f.write("SYSTEM INFORMATION\n")
        f.write("-"*70 + "\n")

        import platform
        import psutil

        f.write(f"OS: {platform.system()} {platform.release()}\n")
        f.write(f"Python: {platform.python_version()}\n")

        mem = psutil.virtual_memory()
        f.write(f"RAM: {mem.total/(1024**3):.1f} GB total, ")
        f.write(f"{mem.available/(1024**3):.1f} GB available\n")

        cpu_percent = psutil.cpu_percent(interval=1)
        f.write(f"CPU Usage: {cpu_percent}%\n\n")

        # Check services
        f.write("SERVICE STATUS\n")
        f.write("-"*70 + "\n")

        import requests

        services = [
            ("Router", "http://localhost:3000/health"),
            ("Ear", "http://localhost:8001/health"),
            ("Brain", "http://localhost:8002/health"),
            ("Styler", "http://localhost:8003/health"),
            ("Voice", "http://localhost:8004/health")
        ]

        for name, url in services:
            try:
                r = requests.get(url, timeout=2)
                status = "ONLINE" if r.status_code == 200 else "ERROR"
                f.write(f"{name:10} [{status:7}] {url}\n")
            except:
                f.write(f"{name:10} [OFFLINE] {url}\n")

        f.write("\n")

        # Model files
        f.write("MODEL FILES\n")
        f.write("-"*70 + "\n")

        models = [
            "D:\\Project\\Brain\\qwen2.5-3b-instruct-q4_k_m.gguf",
            "D:\\Project\\Ear\\adapter_model.safetensors",
            "D:\\Project\\Styler\\adapter_model.safetensors",
            "D:\\Project\\Voice\\model.safetensors"
        ]

        for model_path in models:
            if os.path.exists(model_path):
                size = os.path.getsize(model_path) / (1024**3)
                f.write(f"✓ {os.path.basename(model_path):40} {size:.2f} GB\n")
            else:
                f.write(f"✗ {os.path.basename(model_path):40} NOT FOUND\n")

        f.write("\n" + "="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")

    print(f"Log report created: {report_file}")
    return report_file

if __name__ == "__main__":
    create_log_report()
