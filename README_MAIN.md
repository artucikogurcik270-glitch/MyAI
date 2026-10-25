# Tumaris AI Cluster

🤖 Локальный автономный распределенный ИИ-кластер для обработки каракалпакского и других языков

[![Status](https://img.shields.io/badge/status-production-green.svg)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)]()

---

## 🚀 Быстрый старт

```bash
# 1. Установка зависимостей
install.bat

# 2. Запуск кластера
start_cluster.bat

# 3. Тест системы
python quick_test.py
```

**Готово!** Кластер работает на `http://localhost:3000`

📖 Подробная инструкция: [QUICKSTART.md](QUICKSTART.md)

---

## 📋 Что это?

**Tumaris** - это локальный ИИ-кластер из 4 микросервисов:

| Узел | Порт | Функция | Модель |
|------|------|---------|--------|
| **Router** | 3000 | Маршрутизация | - |
| **Ear** | 8001 | Распознавание речи | Whisper Large V3 |
| **Brain** | 8002 | Языковая модель | Qwen 2.5 3B |
| **Styler** | 8003 | Коррекция текста | Qwen Karakalpak |
| **Voice** | 8004 | Синтез речи | OmniVoice |

```
┌─────────────┐
│   Router    │  ← Единая точка входа
└──────┬──────┘
       │
   ┌───┴───┬───────┬────────┐
   ▼       ▼       ▼        ▼
  Ear    Brain  Styler   Voice
 (STT)   (LLM)  (Grammar) (TTS)
```

---

## 💡 Возможности

✅ **Полностью автономный** - работает без интернета  
✅ **Мультиязычный** - русский, английский, казахский, каракалпакский  
✅ **Голосовой ввод/вывод** - STT + TTS  
✅ **Быстрый** - оптимизирован для CPU  
✅ **Модульный** - каждый узел независим  

---

## 🎯 Примеры использования

### Текстовый запрос

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"type":"text","content":"Сәлем, қалайсыз?","language":"karakalpak"}'
```

### С синтезом речи

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"type":"text","content":"Бул жақсы","language":"karakalpak","synthesize_speech":true}'
```

### Аудио файл

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -F "type=audio" \
  -F "audio=@audio.wav" \
  -F "language=karakalpak"
```

📚 Больше примеров: [API_EXAMPLES.json](API_EXAMPLES.json)

---

## 🛠️ Инструменты

| Скрипт | Назначение |
|--------|-----------|
| `install.bat` | Установка зависимостей |
| `start_cluster.bat` | Запуск кластера |
| `stop_cluster.bat` | Остановка кластера |
| `monitor.bat` | Мониторинг в реальном времени |
| `run_client.bat` | Интерактивный клиент |
| `run_demo.bat` | Демо режим |
| `run_diagnostics.bat` | Диагностика системы |
| `test_cluster.py` | Полный набор тестов |
| `quick_test.py` | Быстрая проверка |
| `benchmark.py` | Тест производительности |

---

## 📊 Системные требования

### Минимальные
- Windows 10/11
- 8 GB RAM
- 4 CPU cores
- 15 GB свободного места

### Рекомендуемые
- 12+ GB RAM
- 8+ CPU cores
- CUDA-совместимый GPU (опционально)

---

## 📖 Документация

| Документ | Описание |
|----------|----------|
| [QUICKSTART.md](QUICKSTART.md) | Быстрый старт за 3 шага |
| [README.md](README.md) | Полное руководство пользователя |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Техническая архитектура |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Руководство разработчика |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Решение проблем |
| [CHANGELOG.md](CHANGELOG.md) | История версий |
| [API_EXAMPLES.json](API_EXAMPLES.json) | Примеры API запросов |

---

## 🔧 Архитектура

### Обработка каракалпакского текста

```
Input → Router → detectKarakalpak() → Styler → Brain → Voice → Output
```

### Обработка общих языков

```
Input → Router → Brain → Output
```

### Обработка аудио

```
Audio → Router → Ear (STT) → Styler → Brain → Voice → Output
```

Подробно: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🧪 Тестирование

```bash
# Быстрый тест (30 сек)
python quick_test.py

# Полный набор тестов (2-3 мин)
python test_cluster.py

# Производительность (5 мин)
python benchmark.py

# Диагностика системы
python diagnostics.py
```

---

## 🐛 Решение проблем

**Проблема:** Порт занят

```bash
netstat -ano | findstr :8002
taskkill /PID <PID> /F
```

**Проблема:** Out of Memory

Уменьшите `n_ctx` в `Brain/service.py` до 1024

**Проблема:** Медленная генерация

Используйте GPU или увеличьте `n_threads`

📖 Полный гайд: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📈 Производительность

| Операция | CPU (8 cores) | GPU (CUDA) |
|----------|---------------|------------|
| Brain генерация | 1.5-3s | 0.5-1s |
| Ear транскрипция | Real-time | Real-time |
| Styler коррекция | 0.5-1s | 0.2-0.5s |
| Voice синтез | 1-2s | 0.5-1s |

---

## 🔐 Безопасность

- ✅ Только localhost доступ
- ✅ Нет внешних API вызовов
- ✅ Изолированные процессы
- ✅ Валидация входных данных

---

## 📦 Используемые технологии

**Backend:**
- Node.js + Express (Router)
- Python + FastAPI (Services)
- llama-cpp-python (Brain)
- Transformers + PEFT (Ear, Styler, Voice)

**Models:**
- Whisper Large V3 + LoRA
- Qwen 2.5 3B Instruct (Q4_K_M)
- Qwen 2.5 3B Karakalpak LoRA
- OmniVoice TTS

---

## 📝 Структура проекта

```
D:\Project\
├── Router/      # Node 1: Gateway (3000)
├── Ear/         # Node 2: STT (8001)
├── Brain/       # Node 3: LLM (8002)
├── Styler/      # Node 4.1: Grammar (8003)
├── Voice/       # Node 4.2: TTS (8004)
├── *.bat        # Deployment scripts
├── *.py         # Testing tools
└── *.md         # Documentation
```

---

## 🎯 Roadmap

**v1.1** (Q1 2027)
- [ ] WebSocket streaming
- [ ] Redis cache
- [ ] Docker support

**v1.2** (Q2 2027)
- [ ] Web UI dashboard
- [ ] Load balancing
- [ ] Multi-speaker TTS

**v2.0** (Q3 2027)
- [ ] Kubernetes
- [ ] Auto-scaling
- [ ] Distributed tracing

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Запустите диагностику: `python diagnostics.py`
3. Соберите логи: `python collect_logs.py`
4. Обратитесь к разработчику

---

## 📄 Лицензия

Private Use - Только для внутреннего использования

---

## 👨‍💻 Автор

Создано для обработки каракалпакского языка  
Версия: 1.0.0  
Дата: 2026-10-25

---

## ⭐ Статус проекта

✅ **Production Ready** - Готов к использованию

---

**© 2026 Tumaris AI Cluster**
