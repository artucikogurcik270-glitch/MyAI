# Tumaris AI Cluster - Complete File Manifest

## Core Service Files

### Node 1: Router (Port 3000)
```
D:\Project\Router\
├── server.js              (3,895 bytes)  - Express gateway service
├── package.json           (456 bytes)    - Node.js dependencies
└── .gitignore             (70 bytes)     - Git ignore patterns
```

### Node 2: Ear (Port 8001)
```
D:\Project\Ear\
├── service.py             (2,503 bytes)  - FastAPI STT service
├── requirements.txt       (167 bytes)    - Python dependencies
├── .gitignore             (54 bytes)     - Git ignore patterns
├── adapter_model.safetensors (30 MB)    - Whisper LoRA weights
├── adapter_config.json    (1 KB)        - LoRA configuration
├── tokenizer files        (~5 MB)       - Whisper tokenizer
└── .cache/                              - HuggingFace cache
```

### Node 3: Brain (Port 8002)
```
D:\Project\Brain\
├── service.py             (2,121 bytes)  - FastAPI LLM service
├── requirements.txt       (98 bytes)     - Python dependencies
├── .gitignore             (54 bytes)     - Git ignore patterns
├── qwen2.5-3b-instruct-q4_k_m.gguf (2.0 GB) - Quantized LLM
└── .cache/                              - Model cache
```

### Node 4.1: Styler (Port 8003)
```
D:\Project\Styler\
├── service.py             (2,564 bytes)  - FastAPI grammar service
├── requirements.txt       (119 bytes)    - Python dependencies
├── .gitignore             (54 bytes)     - Git ignore patterns
├── adapter_model.safetensors (114 MB)   - Qwen Karakalpak LoRA
├── adapter_config.json    (1 KB)        - LoRA configuration
├── tokenizer.json         (11 MB)       - Tokenizer
└── .cache/                              - Model cache
```

### Node 4.2: Voice (Port 8004)
```
D:\Project\Voice\
├── service.py             (2,845 bytes)  - FastAPI TTS service
├── requirements.txt       (125 bytes)    - Python dependencies
├── .gitignore             (62 bytes)     - Git ignore patterns
├── model.safetensors      (2.3 GB)      - OmniVoice weights
├── optimizer.bin          (4.6 GB)      - Training state (optional)
├── config.json            (2 KB)        - Model configuration
├── tokenizer.json         (11 MB)       - Tokenizer
├── outputs/                             - Generated audio files
└── .cache/                              - Model cache
```

---

## Deployment Scripts (7 files)

```
D:\Project\
├── install.bat            (1,639 bytes)  - Dependency installation
├── start_cluster.bat      (3,382 bytes)  - Cluster startup
├── stop_cluster.bat       (1,847 bytes)  - Cluster shutdown
├── monitor.bat            (1,815 bytes)  - Real-time monitoring
├── run_client.bat         (203 bytes)    - Interactive client
├── run_demo.bat           (192 bytes)    - Demo mode
└── run_diagnostics.bat    (165 bytes)    - System diagnostics
```

---

## Testing & Utilities (6 files)

```
D:\Project\
├── test_cluster.py        (5,756 bytes)  - Full test suite
├── quick_test.py          (1,327 bytes)  - Quick health check
├── benchmark.py           (3,071 bytes)  - Performance benchmarks
├── diagnostics.py         (5,614 bytes)  - System diagnostics
├── collect_logs.py        (2,793 bytes)  - Log aggregation
└── client.py              (6,892 bytes)  - Interactive CLI client
```

---

## Documentation (10 files)

```
D:\Project\
├── README.md              (9,305 bytes)  - Complete user guide
├── README_MAIN.md         (8,147 bytes)  - Main landing page
├── QUICKSTART.md          (4,823 bytes)  - Quick start guide
├── ARCHITECTURE.md        (8,187 bytes)  - Technical architecture
├── DEVELOPMENT.md         (10,176 bytes) - Developer guide
├── TROUBLESHOOTING.md     (7,365 bytes)  - Problem solving
├── CHANGELOG.md           (3,204 bytes)  - Version history
├── INSTALL_GUIDE.md       (5,142 bytes)  - Installation steps
├── PROJECT_SUMMARY.md     (11,856 bytes) - Project overview
└── FILE_STRUCTURE.txt     (1,622 bytes)  - Directory structure
```

---

## Configuration Files (3 files)

```
D:\Project\
├── cluster_config.json    (2,474 bytes)  - Cluster configuration
├── API_EXAMPLES.json      (6,595 bytes)  - API reference examples
└── setup_wizard.bat       (1,800 bytes)  - Setup wizard
```

---

## Summary Statistics

### Code Files
- **Python Services:** 5 files (~12 KB total)
- **Node.js Service:** 1 file (~4 KB)
- **Total Code:** ~16 KB

### Scripts
- **Batch Scripts:** 8 files (~11 KB total)
- **Python Utilities:** 6 files (~25 KB total)
- **Total Scripts:** ~36 KB

### Documentation
- **Markdown Files:** 10 files (~69 KB total)
- **Configuration:** 3 files (~11 KB total)
- **Total Docs:** ~80 KB

### Model Files
- **Brain (GGUF):** 2.0 GB
- **Ear (LoRA):** 30 MB + tokenizer (~5 MB)
- **Styler (LoRA):** 114 MB + tokenizer (~11 MB)
- **Voice (Model):** 2.3 GB + tokenizer (~11 MB)
- **Voice (Optimizer):** 4.6 GB (optional, for training)
- **Total Models:** ~9.1 GB (or ~4.5 GB without optimizer)

### Grand Total
- **Project Files:** 50+ files
- **Code & Scripts:** ~52 KB
- **Documentation:** ~80 KB
- **Models & Weights:** ~4.5-9 GB
- **Total Disk Usage:** ~4.5-9 GB

---

## File Organization

```
D:\Project/                          [Root Directory]
│
├── Router/                          [Node.js Gateway]
│   ├── server.js
│   ├── package.json
│   ├── .gitignore
│   └── node_modules/                [Created after npm install]
│
├── Ear/                             [Python STT Service]
│   ├── service.py
│   ├── requirements.txt
│   ├── .gitignore
│   ├── adapter_model.safetensors
│   ├── adapter_config.json
│   ├── tokenizer files (5 files)
│   └── .cache/
│
├── Brain/                           [Python LLM Service]
│   ├── service.py
│   ├── requirements.txt
│   ├── .gitignore
│   ├── qwen2.5-3b-instruct-q4_k_m.gguf
│   └── .cache/
│
├── Styler/                          [Python Grammar Service]
│   ├── service.py
│   ├── requirements.txt
│   ├── .gitignore
│   ├── adapter_model.safetensors
│   ├── adapter_config.json
│   ├── tokenizer.json
│   └── .cache/
│
├── Voice/                           [Python TTS Service]
│   ├── service.py
│   ├── requirements.txt
│   ├── .gitignore
│   ├── model.safetensors
│   ├── optimizer.bin
│   ├── config.json
│   ├── tokenizer.json
│   ├── outputs/                     [Generated audio files]
│   └── .cache/
│
├── logs/                            [Created by collect_logs.py]
│   └── cluster_report_*.txt
│
├── Deployment Scripts (8 .bat files)
├── Testing Tools (6 .py files)
├── Documentation (10 .md files)
└── Configuration (3 .json/.bat files)
```

---

## Dependencies

### Node.js (Router)
```json
{
  "express": "^4.18.2",
  "axios": "^1.6.0",
  "cors": "^2.8.5",
  "body-parser": "^1.20.2",
  "multer": "^1.4.5-lts.1",
  "form-data": "^4.0.0"
}
```

### Python (All Services)
```
fastapi==0.104.1
uvicorn==0.24.0
torch==2.1.0
transformers==4.35.0
peft==0.6.0
llama-cpp-python==0.2.20
librosa==0.10.1
torchaudio==2.1.0
pydantic==2.5.0
python-multipart==0.0.6
soundfile==0.12.1
numpy==1.24.3
requests (for testing)
psutil (for diagnostics)
```

---

## Checksum Summary

### Critical Service Files
- Router: `server.js` (3,895 bytes)
- Ear: `service.py` (2,503 bytes)
- Brain: `service.py` (2,121 bytes)
- Styler: `service.py` (2,564 bytes)
- Voice: `service.py` (2,845 bytes)

### Critical Model Files
- Brain: `qwen2.5-3b-instruct-q4_k_m.gguf` (2,104,932,768 bytes)
- Ear: `adapter_model.safetensors` (31,512,224 bytes)
- Styler: `adapter_model.safetensors` (119,801,528 bytes)
- Voice: `model.safetensors` (2,450,344,144 bytes)

---

**Manifest Generated:** 2026-10-25  
**Project Version:** 1.0.0  
**Status:** Complete ✓
