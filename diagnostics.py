#!/usr/bin/env python3
"""
System information and diagnostics for Tumaris cluster
"""

import platform
import psutil
import sys
import subprocess

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def check_system_info():
    print_section("SYSTEM INFORMATION")

    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Version: {platform.python_version()}")

    # CPU
    cpu_count = psutil.cpu_count(logical=True)
    cpu_physical = psutil.cpu_count(logical=False)
    print(f"\nCPU Cores: {cpu_physical} physical, {cpu_count} logical")

    # RAM
    mem = psutil.virtual_memory()
    print(f"RAM: {mem.total / (1024**3):.1f} GB total")
    print(f"     {mem.available / (1024**3):.1f} GB available")
    print(f"     {mem.percent}% used")

    # Disk
    disk = psutil.disk_usage('D:\\')
    print(f"\nDisk D:\\")
    print(f"  Total: {disk.total / (1024**3):.1f} GB")
    print(f"  Used: {disk.used / (1024**3):.1f} GB")
    print(f"  Free: {disk.free / (1024**3):.1f} GB ({disk.percent}% used)")

def check_dependencies():
    print_section("DEPENDENCIES CHECK")

    # Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        node_version = result.stdout.strip()
        print(f"✓ Node.js: {node_version}")
    except:
        print("✗ Node.js: NOT FOUND")

    # npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        npm_version = result.stdout.strip()
        print(f"✓ npm: {npm_version}")
    except:
        print("✗ npm: NOT FOUND")

    # Python packages
    packages = [
        'fastapi',
        'uvicorn',
        'torch',
        'transformers',
        'peft',
        'llama-cpp-python',
        'librosa',
        'requests'
    ]

    print("\nPython Packages:")
    for pkg in packages:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg}: NOT INSTALLED")

def check_model_files():
    print_section("MODEL FILES CHECK")

    import os

    models = [
        ("Brain GGUF", "D:\\Project\\Brain\\qwen2.5-3b-instruct-q4_k_m.gguf"),
        ("Ear LoRA", "D:\\Project\\Ear\\adapter_model.safetensors"),
        ("Styler LoRA", "D:\\Project\\Styler\\adapter_model.safetensors"),
        ("Voice Model", "D:\\Project\\Voice\\model.safetensors")
    ]

    for name, path in models:
        if os.path.exists(path):
            size_gb = os.path.getsize(path) / (1024**3)
            print(f"✓ {name:15} {size_gb:.2f} GB")
        else:
            print(f"✗ {name:15} NOT FOUND")

def check_gpu():
    print_section("GPU INFORMATION")

    try:
        import torch

        if torch.cuda.is_available():
            print(f"✓ CUDA Available: Yes")
            print(f"  Version: {torch.version.cuda}")
            print(f"  Device Count: {torch.cuda.device_count()}")

            for i in range(torch.cuda.device_count()):
                print(f"\n  GPU {i}: {torch.cuda.get_device_name(i)}")
                props = torch.cuda.get_device_properties(i)
                print(f"    Memory: {props.total_memory / (1024**3):.1f} GB")

                mem_allocated = torch.cuda.memory_allocated(i) / (1024**3)
                mem_reserved = torch.cuda.memory_reserved(i) / (1024**3)
                print(f"    Allocated: {mem_allocated:.2f} GB")
                print(f"    Reserved: {mem_reserved:.2f} GB")
        else:
            print("✗ CUDA Available: No")
            print("  Running on CPU only")

    except ImportError:
        print("✗ PyTorch not installed")

def check_ports():
    print_section("PORT AVAILABILITY")

    ports = [
        (3000, "Router"),
        (8001, "Ear"),
        (8002, "Brain"),
        (8003, "Styler"),
        (8004, "Voice")
    ]

    for port, service in ports:
        connections = [conn for conn in psutil.net_connections() if conn.laddr.port == port]
        if connections:
            print(f"✗ Port {port} ({service}): IN USE")
        else:
            print(f"✓ Port {port} ({service}): Available")

def estimate_requirements():
    print_section("ESTIMATED RESOURCE REQUIREMENTS")

    print("Expected Memory Usage:")
    print("  Brain (Qwen 3B Q4):     ~2.0 GB")
    print("  Ear (Whisper Large):    ~4.0 GB")
    print("  Styler (Qwen LoRA):     ~2.5 GB")
    print("  Voice (OmniVoice):      ~2.5 GB")
    print("  Router + Overhead:      ~1.0 GB")
    print("  " + "-" * 40)
    print("  Total Estimated:       ~12.0 GB")

    mem = psutil.virtual_memory()
    available = mem.available / (1024**3)

    print(f"\nYour Available RAM: {available:.1f} GB")

    if available >= 12.0:
        print("✓ Sufficient memory for full cluster")
    elif available >= 8.0:
        print("⚠ Limited memory - cluster may swap")
    else:
        print("✗ Insufficient memory - cluster will struggle")

def main():
    print("\n" + "="*60)
    print(" TUMARIS CLUSTER - SYSTEM DIAGNOSTICS")
    print("="*60)

    check_system_info()
    check_dependencies()
    check_model_files()
    check_gpu()
    check_ports()
    estimate_requirements()

    print("\n" + "="*60)
    print(" DIAGNOSTICS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.\n")
    except Exception as e:
        print(f"\n\nError during diagnostics: {e}\n")
