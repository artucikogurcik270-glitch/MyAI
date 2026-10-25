# Tumaris AI Cluster - Архитектурная документация

## Обзор системы

Tumaris - это локальный автономный ИИ-кластер, построенный по принципу «bee-hive microservices». Система работает полностью оффлайн без зависимости от внешних API.

## Архитектурные принципы

### 1. Микросервисная архитектура

Каждый узел - это независимый сервис со своим:
- API интерфейсом (REST)
- Портом
- Моделью ИИ
- Логикой обработки

```
                    ┌─────────────┐
                    │   Client    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Router    │ ◄── Единая точка входа
                    │   Node 1    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐      ┌────▼────┐
    │   Ear   │       │  Brain  │      │ Styler  │
    │ Node 2  │       │ Node 3  │      │ Node 4.1│
    └─────────┘       └────┬────┘      └─────────┘
                           │
                      ┌────▼────┐
                      │  Voice  │
                      │ Node 4.2│
                      └─────────┘
```

### 2. Языковая маршрутизация

**Каракалпакский язык:**
```
Запрос → Router → detectKarakalpak() → True
                        ↓
            Ear (если audio) → Styler → Brain → Voice (опционально)
```

**Общие языки (RU, EN, KK):**
```
Запрос → Router → detectKarakalpak() → False
                        ↓
                      Brain
```

### 3. Протокол взаимодействия

Все узлы общаются через HTTP REST API:

```
POST /api/v1/process
├── Content-Type: application/json
├── Body: { type, content, language }
└── Response: { status, response, ... }
```

### 4. Модели и квантизация

| Узел | Модель | Размер | Квантизация | Назначение |
|------|--------|--------|-------------|------------|
| Ear | Whisper Large V3 + LoRA | ~4 GB | FP16/BF16 | STT каракалпакский |
| Brain | Qwen 2.5 3B Instruct | ~2 GB | Q4_K_M (GGUF) | Универсальная LLM |
| Styler | Qwen 2.5 3B + LoRA | ~3 GB | FP16 + LoRA | Коррекция каракалпакского |
| Voice | OmniVoice | ~2.5 GB | FP16/FP32 | TTS каракалпакский |

**Преимущества квантизации:**
- Brain использует Q4_K_M → экономия 75% памяти
- Минимальная потеря качества (<3%)
- Быстрый инференс на CPU

### 5. Обработка ошибок

Каждый узел реализует:

```python
try:
    # Основная логика
    result = process()
    return {"status": "success", "data": result}
except Exception as e:
    return {"status": "error", "message": str(e)}
```

Router ловит ошибки от подчиненных сервисов:

```javascript
try {
    const response = await axios.post(...)
} catch (error) {
    return res.status(500).json({
        status: 'error',
        message: error.message
    })
}
```

### 6. Масштабируемость

#### Горизонтальное масштабирование:

```
Router (3000)
    ↓
┌───────┬───────┬───────┐
Brain   Brain   Brain     ← Load balancing
8002    8012    8022
```

#### Вертикальное масштабирование:

- Увеличение `n_ctx` (контекст)
- Больше потоков `n_threads`
- GPU offloading `n_gpu_layers`

### 7. Кэширование и оптимизация

**Brain (llama-cpp):**
```python
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,           # Размер контекста
    n_threads=8,          # Параллельные потоки
    n_gpu_layers=0,       # GPU слои (0=CPU only)
    use_mmap=True,        # Memory mapping
    use_mlock=True        # Lock in RAM
)
```

**Transformers (Ear, Styler, Voice):**
```python
model.eval()              # Evaluation mode
with torch.no_grad():     # No gradient calculation
    output = model(...)   # Faster inference
```

### 8. Безопасность

**Изоляция:**
- Каждый сервис в своем процессе
- Crash одного узла не влияет на другие
- Localhost-only доступ

**Валидация:**
```python
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512      # Ограничение
    temperature: float = 0.7   # Валидация типов
```

### 9. Мониторинг

**Health checks:**
```bash
GET /health
→ {"status": "ok", "service": "brain", "port": 8002}
```

**Логирование:**
```python
print(f"[BRAIN] Generating response for: {prompt[:100]}...")
print(f"[BRAIN] Generated: {response[:100]}...")
```

### 10. Типы данных и контракты

**Общий формат ответа:**
```typescript
interface Response {
    status: "success" | "error"
    input_text?: string
    processed_text?: string
    response?: string
    language?: "karakalpak" | "general"
    audio_url?: string
    message?: string    // Для ошибок
}
```

## Развертывание

### Последовательность запуска:

1. **Brain** (самый долгий) → 30-45 сек
2. **Ear** (Whisper) → 15-20 сек
3. **Styler** → 10-15 сек
4. **Voice** → 10-15 сек
5. **Router** (мгновенно) → 1-2 сек

Общее время старта: ~70 секунд

### Зависимости между узлами:

```
Router зависит от → Ear, Brain, Styler, Voice
Ear независим
Brain независим
Styler независим
Voice независим
```

## Будущие улучшения

### Фаза 2:
- [ ] WebSocket для streaming ответов
- [ ] Redis для кэширования
- [ ] Batch processing для эффективности
- [ ] Метрики (Prometheus)

### Фаза 3:
- [ ] Kubernetes deployment
- [ ] Auto-scaling
- [ ] Distributed tracing
- [ ] A/B testing моделей

## Диаграммы

### Dataflow для каракалпакского текста:

```
User Input (text)
    ↓
Router (detect language=karakalpak)
    ↓
Styler (grammar correction)
    ↓
Brain (generate response)
    ↓
Voice (optional TTS)
    ↓
Return to User
```

### Dataflow для аудио:

```
User Input (audio file)
    ↓
Router (type=audio)
    ↓
Ear (transcribe → text)
    ↓
Styler (grammar correction)
    ↓
Brain (generate response)
    ↓
Voice (optional TTS)
    ↓
Return to User
```

## Технические детали

### Порты и протоколы:

| Порт | Сервис | Протокол | Framework |
|------|--------|----------|-----------|
| 3000 | Router | HTTP | Express.js |
| 8001 | Ear | HTTP | FastAPI |
| 8002 | Brain | HTTP | FastAPI |
| 8003 | Styler | HTTP | FastAPI |
| 8004 | Voice | HTTP | FastAPI |

### Форматы данных:

- **Text**: JSON (UTF-8)
- **Audio**: Multipart form-data (WAV, MP3)
- **Models**: GGUF (Brain), SafeTensors (остальные)

---

**Дата создания:** 2026-10-25  
**Версия:** 1.0.0  
**Статус:** Production Ready
