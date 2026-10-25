# TUMARIS AI CLUSTER - INSTALLATION GUIDE

## Пошаговая инструкция по установке и запуску

---

## Шаг 1: Предварительные требования

### Проверьте установленное ПО

#### 1.1 Node.js
```bash
node --version
```
Должен быть 18.0.0 или выше

Если не установлен:
- Скачать с https://nodejs.org/
- Установить LTS версию
- Перезапустить командную строку

#### 1.2 Python
```bash
python --version
```
Должен быть 3.10.0 или выше

Если не установлен:
- Скачать с https://www.python.org/
- При установке отметить "Add Python to PATH"
- Перезапустить командную строку

#### 1.3 pip
```bash
pip --version
```
Должен быть установлен вместе с Python

---

## Шаг 2: Установка зависимостей

### 2.1 Автоматическая установка (РЕКОМЕНДУЕТСЯ)

```bash
cd D:\Project
install.bat
```

Это установит:
- Пакеты Node.js для Router
- Пакеты Python для всех AI сервисов

⏱️ Время установки: 5-10 минут

### 2.2 Ручная установка (если автоматическая не сработала)

#### Router (Node.js)
```bash
cd D:\Project\Router
npm install
```

#### Ear Service
```bash
cd D:\Project\Ear
pip install -r requirements.txt
```

#### Brain Service
```bash
cd D:\Project\Brain
pip install -r requirements.txt
```

#### Styler Service
```bash
cd D:\Project\Styler
pip install -r requirements.txt
```

#### Voice Service
```bash
cd D:\Project\Voice
pip install -r requirements.txt
```

---

## Шаг 3: Проверка моделей

Убедитесь что все файлы моделей на месте:

```bash
python diagnostics.py
```

Должны быть найдены:
- ✓ Brain: qwen2.5-3b-instruct-q4_k_m.gguf (~2 GB)
- ✓ Ear: adapter_model.safetensors (~30 MB)
- ✓ Styler: adapter_model.safetensors (~114 MB)
- ✓ Voice: model.safetensors (~2.3 GB)

---

## Шаг 4: Запуск кластера

### 4.1 Автоматический запуск

```bash
cd D:\Project
start_cluster.bat
```

Откроются 5 окон консоли:
1. Tumaris-Brain (Port 8002) - загружается первым
2. Tumaris-Ear (Port 8001)
3. Tumaris-Styler (Port 8003)
4. Tumaris-Voice (Port 8004)
5. Tumaris-Router (Port 3000) - запускается последним

⏱️ Время запуска: 60-90 секунд

### 4.2 Ручной запуск (для отладки)

**Окно 1 - Brain:**
```bash
cd D:\Project\Brain
python service.py
```

**Окно 2 - Ear:**
```bash
cd D:\Project\Ear
python service.py
```

**Окно 3 - Styler:**
```bash
cd D:\Project\Styler
python service.py
```

**Окно 4 - Voice:**
```bash
cd D:\Project\Voice
python service.py
```

**Окно 5 - Router:**
```bash
cd D:\Project\Router
node server.js
```

---

## Шаг 5: Проверка работы

### 5.1 Быстрая проверка

```bash
python quick_test.py
```

Ожидаемый результат:
```
✓ Router is online
✓ Brain is working
✅ Cluster is working correctly!
```

### 5.2 Полная проверка

```bash
python test_cluster.py
```

Запускает 5 тестов:
1. Health check всех сервисов
2. Обработка общих языков
3. Обработка каракалпакского языка
4. Автоопределение языка
5. Нагрузочное тестирование

### 5.3 Проверка через браузер

Откройте в браузере:
- http://localhost:3000/health - Router
- http://localhost:8001/docs - Ear API docs
- http://localhost:8002/docs - Brain API docs
- http://localhost:8003/docs - Styler API docs
- http://localhost:8004/docs - Voice API docs

---

## Шаг 6: Первый запрос

### 6.1 Через curl

```bash
curl -X POST http://localhost:3000/api/v1/process ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"text\",\"content\":\"Привет, как дела?\",\"language\":\"ru\"}"
```

### 6.2 Через интерактивный клиент

```bash
run_client.bat
```

Введите текст и нажмите Enter

---

## Шаг 7: Мониторинг

```bash
monitor.bat
```

Покажет статус всех узлов в реальном времени

---

## Остановка кластера

```bash
stop_cluster.bat
```

Или закройте все окна консоли (Ctrl+C в каждом)

---

## Troubleshooting

### Проблема: "Port already in use"

**Решение:**
```bash
stop_cluster.bat
```

Если не помогло:
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Проблема: "Module not found"

**Решение:**
```bash
# Для Python
pip install --upgrade pip
pip install -r requirements.txt

# Для Node.js
cd Router
npm install
```

### Проблема: "Model file not found"

**Решение:**
Проверьте что все файлы моделей находятся в правильных папках:
```bash
dir D:\Project\Brain\*.gguf
dir D:\Project\Ear\*.safetensors
dir D:\Project\Styler\*.safetensors
dir D:\Project\Voice\*.safetensors
```

### Проблема: Медленная работа

**Решение:**
1. Закройте другие приложения
2. Уменьшите n_ctx в Brain/service.py
3. Используйте GPU (если доступен)

---

## Проверочный список

Перед началом работы убедитесь:

- [ ] Node.js 18+ установлен
- [ ] Python 3.10+ установлен
- [ ] Все зависимости установлены (install.bat)
- [ ] Все файлы моделей на месте
- [ ] Порты 3000, 8001-8004 свободны
- [ ] Достаточно RAM (12+ GB рекомендуется)
- [ ] Кластер запущен (start_cluster.bat)
- [ ] Тест прошел успешно (quick_test.py)

---

## Полезные команды

```bash
# Диагностика системы
python diagnostics.py

# Быстрый тест
python quick_test.py

# Полное тестирование
python test_cluster.py

# Бенчмарк производительности
python benchmark.py

# Сбор логов
python collect_logs.py

# Интерактивный клиент
run_client.bat

# Демо режим
run_demo.bat

# Мониторинг
monitor.bat
```

---

## Поддержка

При проблемах:
1. Проверьте TROUBLESHOOTING.md
2. Запустите diagnostics.py
3. Проверьте логи в окнах сервисов
4. Соберите логи: collect_logs.py

---

**Готово! Кластер Tumaris установлен и готов к работе! 🎉**
