# Tumaris Troubleshooting Guide

## Типичные проблемы и решения

### 1. Порты заняты

**Проблема:** Ошибка "Address already in use" или "Port already allocated"

**Решение:**

```bash
# Найти процесс на порту
netstat -ano | findstr :8002

# Завершить процесс (замените <PID> на ID процесса)
taskkill /PID <PID> /F

# Или остановить все сервисы Tumaris
stop_cluster.bat
```

### 2. Out of Memory (OOM)

**Проблема:** Python процесс завершается с ошибкой памяти

**Решение 1 - Уменьшить контекст в Brain:**

Отредактировать `D:\Project\Brain\service.py`:
```python
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,  # Было 2048
    n_threads=8,
    n_gpu_layers=0
)
```

**Решение 2 - Использовать GPU:**

Установить CUDA версию llama-cpp-python:
```bash
pip install llama-cpp-python --force-reinstall --no-cache-dir --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

Изменить в `service.py`:
```python
n_gpu_layers=35  # Вместо 0
```

### 3. Модели не загружаются

**Проблема:** FileNotFoundError или "Model not found"

**Проверка:**

```bash
# Проверить наличие файлов моделей
dir D:\Project\Brain\*.gguf
dir D:\Project\Ear\adapter_model.safetensors
dir D:\Project\Styler\adapter_model.safetensors
dir D:\Project\Voice\model.safetensors
```

**Решение:** Убедитесь что все файлы моделей на месте согласно ТЗ.

### 4. Медленная генерация

**Проблема:** Brain очень медленно генерирует ответы (>10 сек)

**Решение 1 - Использовать больше потоков:**

```python
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=16,  # Увеличить до количества ядер CPU
    n_gpu_layers=0
)
```

**Решение 2 - Использовать GPU (CUDA):**

См. раздел "Out of Memory" выше.

**Решение 3 - Уменьшить max_tokens:**

```json
{
  "prompt": "Ваш промпт",
  "max_tokens": 256  // Вместо 512
}
```

### 5. Router не может подключиться к сервисам

**Проблема:** "ECONNREFUSED" или "Connection refused"

**Решение:**

```bash
# Проверить что все сервисы запущены
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health

# Если какой-то не отвечает, перезапустить
stop_cluster.bat
start_cluster.bat
```

### 6. Ошибка при установке зависимостей

**Проблема:** npm install или pip install завершается с ошибкой

**Решение для Node.js:**

```bash
cd D:\Project\Router
npm cache clean --force
npm install
```

**Решение для Python:**

```bash
# Обновить pip
python -m pip install --upgrade pip

# Переустановить с чистого листа
pip cache purge
pip install -r requirements.txt
```

### 7. CUDA / GPU не обнаружен

**Проблема:** torch.cuda.is_available() возвращает False

**Решение:**

```bash
# Проверить версию PyTorch
python -c "import torch; print(torch.__version__)"

# Переустановить PyTorch с CUDA 11.8
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 8. Whisper не распознает аудио

**Проблема:** Транскрипция возвращает пустой текст или ошибку

**Решение:**

```python
# Убедиться что аудио в правильном формате
# В service.py Ear добавить логирование

audio_array, sampling_rate = librosa.load(audio_path, sr=16000)
print(f"Audio shape: {audio_array.shape}, SR: {sampling_rate}")  # Debug
```

Поддерживаемые форматы: WAV, MP3, FLAC, OGG
Рекомендуемые параметры: 16kHz, mono

### 9. Ошибка импорта модулей Python

**Проблема:** ModuleNotFoundError для transformers, peft и т.д.

**Решение:**

```bash
# Проверить установленные пакеты
pip list | findstr transformers

# Переустановить конкретный пакет
pip install --force-reinstall transformers==4.35.0
```

### 10. Node.js "Cannot find module"

**Проблема:** Router не может найти express, axios и т.д.

**Решение:**

```bash
cd D:\Project\Router

# Удалить node_modules и переустановить
rmdir /s /q node_modules
del package-lock.json
npm install
```

### 11. FastAPI Swagger UI не открывается

**Проблема:** http://localhost:8001/docs не загружается

**Причина:** Сервис еще загружает модель

**Решение:** Подождать 30-60 секунд после запуска. Проверить логи в окне сервиса.

### 12. Автоопределение языка работает неправильно

**Проблема:** Каракалпакский текст определяется как общий язык

**Решение:** Использовать явное указание языка:

```json
{
  "type": "text",
  "content": "Ваш текст",
  "language": "karakalpak"  // Явно указать
}
```

Или улучшить функцию detectKarakalpak() в Router/server.js

### 13. Проверка логов

Каждый сервис выводит логи в свое окно консоли:

- `[ROUTER]` - Node 1
- `[EAR]` - Node 2
- `[BRAIN]` - Node 3
- `[STYLER]` - Node 4.1
- `[VOICE]` - Node 4.2

Следите за этими логами для диагностики проблем.

### 14. Тестирование отдельных узлов

```bash
# Тест Brain
curl -X POST http://localhost:8002/generate -H "Content-Type: application/json" -d "{\"prompt\":\"test\"}"

# Тест Styler
curl -X POST http://localhost:8003/style -H "Content-Type: application/json" -d "{\"text\":\"test\"}"

# Тест Voice
curl -X POST http://localhost:8004/synthesize -H "Content-Type: application/json" -d "{\"text\":\"test\"}"
```

### 15. Полный сброс

Если ничего не помогает:

```bash
# 1. Остановить все
stop_cluster.bat

# 2. Завершить все Python процессы
taskkill /IM python.exe /F
taskkill /IM node.exe /F

# 3. Переустановить зависимости
install.bat

# 4. Перезапустить
start_cluster.bat
```

## Контакты поддержки

При возникновении проблем, которые не описаны в этом руководстве, обратитесь к разработчику с подробным описанием ошибки и логами из консоли.
