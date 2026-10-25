# Tumaris Development Guide

## Для разработчиков

Это руководство для разработчиков, которые хотят модифицировать или расширить кластер Tumaris.

---

## Архитектура кода

### Router (Node.js)

**Файл:** `D:\Project\Router\server.js`

**Основные функции:**

```javascript
// Определение каракалпакского языка
function detectKarakalpak(text) {
  const karakalpakPatterns = [
    /[әөүғқңһ]/i,
    /\b(бул|мен|сен|ол|биз|сиз|олар)\b/i
  ];
  return karakalpakPatterns.some(pattern => pattern.test(text));
}

// Главный endpoint
app.post('/api/v1/process', async (req, res) => {
  // 1. Получить input (текст или аудио)
  // 2. Определить язык
  // 3. Роутинг по узлам
  // 4. Вернуть результат
})
```

**Как добавить новый маршрут:**

```javascript
app.post('/api/v1/custom', async (req, res) => {
  try {
    // Ваша логика
    res.json({ status: 'success', data: result });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
});
```

---

### Brain Service (Python)

**Файл:** `D:\Project\Brain\service.py`

**Основные компоненты:**

```python
# Загрузка модели
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,        # Размер контекста
    n_threads=8,       # Потоки CPU
    n_gpu_layers=0,    # GPU offloading
    verbose=False
)

# Генерация
output = llm(
    prompt,
    max_tokens=512,
    temperature=0.7,
    stop=["<|im_end|>"]
)
```

**Как изменить промпт систему:**

```python
system_prompt = "Вы - полезный ИИ ассистент..."

full_prompt = f"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""
```

---

### Ear Service (Whisper)

**Файл:** `D:\Project\Ear\service.py`

**Загрузка адаптера:**

```python
# Базовая модель
base_model = WhisperForConditionalGeneration.from_pretrained(
    BASE_MODEL,
    cache_dir=os.path.join(MODEL_PATH, ".cache")
)

# Применение LoRA
model = PeftModel.from_pretrained(base_model, MODEL_PATH)
model = model.to(device)
model.eval()
```

**Добавление препроцессинга:**

```python
# Перед inference
audio_array, sr = librosa.load(audio_path, sr=16000)

# Ваша обработка
audio_array = apply_noise_reduction(audio_array)
audio_array = normalize_volume(audio_array)

# Затем inference
input_features = processor(audio_array, ...).input_features
```

---

### Styler Service (Grammar Correction)

**Файл:** `D:\Project\Styler\service.py`

**Кастомизация промпта:**

```python
prompt = f"""Исправьте грамматику и стилистику:

{request.text}

Исправленный текст:"""

# Или другой формат
prompt = f"""<|im_start|>system
Вы - редактор каракалпакского языка.<|im_end|>
<|im_start|>user
{request.text}<|im_end|>
<|im_start|>assistant
"""
```

---

### Voice Service (TTS)

**Файл:** `D:\Project\Voice\service.py`

**Параметры синтеза:**

```python
@app.post("/synthesize")
async def synthesize_speech(request: SynthesizeRequest):
    # request.text - текст
    # request.speaker_id - ID говорящего
    # request.speed - скорость речи
    
    # Генерация аудио
    audio_features = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7
    )
```

---

## Расширение функциональности

### 1. Добавление нового языка

**В Router/server.js:**

```javascript
function detectNewLanguage(text) {
  // Паттерны вашего языка
  const patterns = [...];
  return patterns.some(p => p.test(text));
}

// В обработчике
if (detectNewLanguage(inputText)) {
  // Специальная обработка
}
```

### 2. Добавление кэширования

**Пример Redis cache:**

```python
import redis

cache = redis.Redis(host='localhost', port=6379)

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    # Проверить кэш
    cache_key = f"brain:{hash(request.prompt)}"
    cached = cache.get(cache_key)
    
    if cached:
        return JSONResponse(json.loads(cached))
    
    # Генерация
    result = llm(request.prompt, ...)
    
    # Сохранить в кэш
    cache.setex(cache_key, 3600, json.dumps(result))
    
    return result
```

### 3. Добавление WebSocket

**FastAPI WebSocket пример:**

```python
from fastapi import WebSocket

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        
        # Streaming generation
        for token in llm.generate_stream(data):
            await websocket.send_text(token)
```

### 4. Batch Processing

**Обработка нескольких запросов:**

```python
@app.post("/generate_batch")
async def generate_batch(requests: List[GenerateRequest]):
    results = []
    
    for req in requests:
        output = llm(req.prompt, ...)
        results.append(output)
    
    return {"results": results}
```

---

## Оптимизация производительности

### 1. GPU Acceleration

**Для llama-cpp (Brain):**

```bash
# Переустановить с CUDA
pip install llama-cpp-python --force-reinstall --no-cache-dir --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

# В коде
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=35,  # Все слои на GPU
    ...
)
```

**Для Transformers (Ear, Styler, Voice):**

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Оптимизация
model.half()  # FP16
torch.backends.cudnn.benchmark = True
```

### 2. Параллельная обработка

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.post("/process_parallel")
async def process_parallel(requests: List[Request]):
    futures = [executor.submit(process_one, req) for req in requests]
    results = [f.result() for f in futures]
    return results
```

### 3. Model Quantization

**Для новых моделей:**

```bash
# GGUF quantization
python convert.py model.safetensors
./quantize model.gguf model_q4.gguf q4_k_m
```

---

## Debugging

### Включение verbose логирования

**Brain:**

```python
llm = Llama(
    model_path=MODEL_PATH,
    verbose=True  # Детальные логи
)
```

**Transformers:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Профилирование

```python
import cProfile
import pstats

def profile_generate():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Ваш код
    output = llm(prompt, ...)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

---

## Тестирование

### Unit тесты

```python
import pytest

def test_brain_generation():
    payload = {"prompt": "test", "max_tokens": 10}
    response = client.post("/generate", json=payload)
    
    assert response.status_code == 200
    assert "response" in response.json()

def test_styler_correction():
    payload = {"text": "тест"}
    response = client.post("/style", json=payload)
    
    assert response.status_code == 200
    assert "styled_text" in response.json()
```

### Integration тесты

```python
def test_full_pipeline():
    # Отправить через Router
    payload = {
        "type": "text",
        "content": "Сәлем",
        "language": "karakalpak"
    }
    
    response = requests.post(
        "http://localhost:3000/api/v1/process",
        json=payload
    )
    
    assert response.status_code == 200
    result = response.json()
    
    # Проверить что прошло через Styler
    assert result["processed_text"] != result["input_text"]
    
    # Проверить что Brain ответил
    assert len(result["response"]) > 0
```

---

## Развертывание

### Docker (будущее)

```dockerfile
# Brain service
FROM python:3.10
WORKDIR /app
COPY Brain/ .
RUN pip install -r requirements.txt
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8002"]
```

### systemd service (Linux)

```ini
[Unit]
Description=Tumaris Brain Service

[Service]
Type=simple
WorkingDirectory=/opt/tumaris/Brain
ExecStart=/usr/bin/python3 service.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Безопасность

### Rate limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate")
@limiter.limit("10/minute")
async def generate_text(request: Request, ...):
    ...
```

### Input validation

```python
from pydantic import BaseModel, validator

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if len(v) > 10000:
            raise ValueError('Prompt too long')
        return v
    
    @validator('max_tokens')
    def validate_tokens(cls, v):
        if v > 2048:
            raise ValueError('Too many tokens')
        return v
```

---

## Контрибуция

При внесении изменений:

1. Тестируйте локально
2. Обновляйте документацию
3. Следуйте стилю кода
4. Добавляйте логирование
5. Обрабатывайте ошибки

---

**Версия:** 1.0.0  
**Обновлено:** 2026-10-25
