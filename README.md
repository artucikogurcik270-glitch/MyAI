# Tumaris AI Cluster

Локальный автономный распределенный гибридный ИИ-кластер для обработки каракалпакского и общих языков.

## Архитектура

Система состоит из 4 микросервисных узлов:

```
┌─────────────────────────────────────────────────────────────┐
│                    Node 1: Router (Port 3000)               │
│              Маршрутизация и определение языка              │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
     ┌───────▼──────┐                ┌────────▼────────┐
     │  Node 2: Ear │                │ Node 3: Brain   │
     │  Port 8001   │                │   Port 8002     │
     │   Whisper    │                │  Qwen 3B GGUF   │
     │ STT Service  │                │  LLM Inference  │
     └──────────────┘                └─────────────────┘
                                              │
                        ┌─────────────────────┴─────────────┐
                        │                                   │
              ┌─────────▼──────────┐           ┌──────────▼─────────┐
              │ Node 4.1: Styler   │           │ Node 4.2: Voice    │
              │    Port 8003       │           │    Port 8004       │
              │ Qwen Karakalpak    │           │ OmniVoice TTS      │
              │  Grammar Corrector │           │  Speech Synthesis  │
              └────────────────────┘           └────────────────────┘
```

## Технологический стек

| Узел | Технологии | Модель | Размер |
|------|-----------|--------|--------|
| Router | Node.js, Express | - | - |
| Ear | Python, FastAPI, Transformers | Whisper Large V3 LoRA | ~4 GB |
| Brain | Python, FastAPI, llama-cpp | Qwen 2.5 3B Q4_K_M | ~2 GB |
| Styler | Python, FastAPI, PyTorch | Qwen 2.5 3B Karakalpak | ~3 GB |
| Voice | Python, FastAPI, TTS | OmniVoice Karakalpak | ~2.5 GB |

## Установка

1. **Предварительные требования:**
   - Node.js 18+
   - Python 3.10+
   - 12+ GB RAM
   - CUDA (опционально, для GPU ускорения)

2. **Установка зависимостей:**

```bash
# Запустить скрипт установки
install.bat
```

Этот скрипт установит все необходимые пакеты для всех узлов.

## Запуск кластера

```bash
# Запуск всех узлов
start_cluster.bat
```

Скрипт последовательно запустит все сервисы:
- Brain (8002) - первым, т.к. самый медленный для загрузки
- Ear (8001)
- Styler (8003)
- Voice (8004)
- Router (3000) - последним

## Остановка кластера

```bash
# Остановка всех узлов
stop_cluster.bat
```

## API Эндпоинты

### Главный эндпоинт (Router)

**POST** `http://localhost:3000/api/v1/process`

#### Запрос (JSON):

```json
{
  "type": "text",
  "content": "Ваш текст или путь к аудиофайлу",
  "language": "auto",
  "max_tokens": 512,
  "temperature": 0.7,
  "synthesize_speech": false
}
```

#### Параметры:
- `type`: "text" | "audio"
- `content`: текст запроса или аудио
- `language`: "auto" | "karakalpak" | "ru" | "en"
- `synthesize_speech`: true/false (озвучивать ответ)

#### Ответ:

```json
{
  "status": "success",
  "input_text": "Исходный текст",
  "processed_text": "Обработанный текст",
  "response": "Ответ модели",
  "language": "karakalpak",
  "audio_url": "/static/output.wav"
}
```

### Отдельные узлы

#### Node 2: Ear Service

**POST** `http://localhost:8001/transcribe`

Загрузка аудиофайла (multipart/form-data)

#### Node 3: Brain Service

**POST** `http://localhost:8002/generate`

```json
{
  "prompt": "Ваш промпт",
  "max_tokens": 512,
  "temperature": 0.7
}
```

#### Node 4.1: Styler Service

**POST** `http://localhost:8003/style`

```json
{
  "text": "Текст для коррекции"
}
```

#### Node 4.2: Voice Service

**POST** `http://localhost:8004/synthesize`

```json
{
  "text": "Текст для озвучки"
}
```

## Тестирование

Запустить полный набор тестов:

```bash
cd D:\Project
python test_cluster.py
```

Тесты проверяют:
1. Health check всех узлов
2. Обработку общих языков (русский, английский)
3. Обработку каракалпакского языка
4. Автоопределение языка
5. Нагрузочное тестирование

## Примеры использования

### Пример 1: Русский текст (через Brain)

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "content": "Расскажи про искусственный интеллект",
    "language": "ru"
  }'
```

### Пример 2: Каракалпакский текст (полная обработка)

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "content": "Сәлем, қалайсыз?",
    "language": "karakalpak",
    "synthesize_speech": true
  }'
```

### Пример 3: Аудио транскрипция

```bash
curl -X POST http://localhost:3000/api/v1/process \
  -F "type=audio" \
  -F "audio=@audio.wav" \
  -F "language=karakalpak"
```

## Структура файлов

```
D:\Project\
│
├── Router\
│   ├── server.js          # Node.js сервер
│   └── package.json       # Зависимости
│
├── Ear\
│   ├── service.py         # FastAPI сервис
│   ├── requirements.txt   # Python зависимости
│   ├── adapter_model.safetensors
│   └── ... (Whisper weights)
│
├── Brain\
│   ├── service.py
│   ├── requirements.txt
│   └── qwen2.5-3b-instruct-q4_k_m.gguf
│
├── Styler\
│   ├── service.py
│   ├── requirements.txt
│   └── adapter_model.safetensors
│
├── Voice\
│   ├── service.py
│   ├── requirements.txt
│   └── model.safetensors
│
├── install.bat            # Установка всех зависимостей
├── start_cluster.bat      # Запуск кластера
├── stop_cluster.bat       # Остановка кластера
└── test_cluster.py        # Тесты
```

## Производительность

### Требования к ресурсам:

- **RAM**: 10-12 GB (пиковое)
- **Storage**: ~15 GB (модели)
- **CPU**: 8+ cores рекомендуется
- **GPU**: Опционально (ускорение в 5-10x)

### Время отклика:

- Brain (CPU): 1.5-3 секунды на генерацию
- Ear (CPU): Real-time или быстрее
- Styler (CPU): ~0.5-1 секунда
- Voice (CPU): ~1-2 секунды

## Логирование

Каждый узел выводит логи в свое окно командной строки:
- `[ROUTER]` - маршрутизация запросов
- `[EAR]` - транскрипция аудио
- `[BRAIN]` - генерация ответов
- `[STYLER]` - стилистическая обработка
- `[VOICE]` - синтез речи

## Troubleshooting

### Проблема: Узел не запускается

```bash
# Проверить доступность порта
netstat -ano | findstr :8002

# Завершить процесс, если порт занят
taskkill /PID <PID> /F
```

### Проблема: Out of Memory

- Уменьшить `n_ctx` в Brain service
- Использовать GPU вместо CPU
- Запускать узлы по отдельности

### Проблема: Медленная генерация

- Использовать GPU
- Уменьшить `max_tokens`
- Использовать меньшую модель

## Лицензия

Этот проект создан для локального использования.

## Контакты

Для вопросов и предложений обращайтесь к разработчику.
