# Tumaris AI Cluster - Quick Start Guide

## 🚀 Быстрый старт за 3 шага

### Шаг 1: Установка зависимостей

```bash
# Перейдите в папку проекта
cd D:\Project

# Запустите установку
install.bat
```

⏱️ Время установки: ~5-10 минут

### Шаг 2: Запуск кластера

```bash
start_cluster.bat
```

⏱️ Время запуска: ~60-90 секунд

Откроются 5 окон консоли - по одному для каждого узла.

### Шаг 3: Тестирование

```bash
# Быстрый тест
python quick_test.py

# Или полный тест
python test_cluster.py

# Или интерактивный режим
run_client.bat
```

---

## 📊 Статус проверка

```bash
# Мониторинг в реальном времени
monitor.bat
```

Или вручную:
```bash
curl http://localhost:3000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

---

## 💡 Примеры использования

### Пример 1: Простой текстовый запрос

```bash
curl -X POST http://localhost:3000/api/v1/process ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"text\",\"content\":\"Привет, как дела?\",\"language\":\"ru\"}"
```

### Пример 2: Каракалпакский текст

```bash
curl -X POST http://localhost:3000/api/v1/process ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"text\",\"content\":\"Сәлем, қалайсыз?\",\"language\":\"karakalpak\"}"
```

### Пример 3: С синтезом речи

```bash
curl -X POST http://localhost:3000/api/v1/process ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"text\",\"content\":\"Бул жақсы\",\"language\":\"karakalpak\",\"synthesize_speech\":true}"
```

### Пример 4: Аудио файл

```bash
curl -X POST http://localhost:3000/api/v1/process ^
  -F "type=audio" ^
  -F "audio=@audio.wav" ^
  -F "language=karakalpak"
```

---

## 🎮 Интерактивный клиент

```bash
run_client.bat
```

Команды в интерактивном режиме:
- Просто введите текст для обработки
- `/ru <текст>` - Принудительно русский
- `/kk <текст>` - Принудительно каракалпакский
- `/voice <текст>` - С озвучкой
- `/status` - Проверить статус
- `/quit` - Выход

---

## 🛑 Остановка кластера

```bash
stop_cluster.bat
```

---

## 📁 Структура проекта

```
D:\Project\
│
├── Router\           # Node 1: Маршрутизатор (3000)
├── Ear\              # Node 2: Распознавание речи (8001)
├── Brain\            # Node 3: Языковая модель (8002)
├── Styler\           # Node 4.1: Коррекция текста (8003)
├── Voice\            # Node 4.2: Синтез речи (8004)
│
├── start_cluster.bat # Запуск кластера
├── stop_cluster.bat  # Остановка кластера
├── install.bat       # Установка зависимостей
├── monitor.bat       # Мониторинг
├── test_cluster.py   # Тесты
├── client.py         # Интерактивный клиент
│
├── README.md         # Полная документация
├── ARCHITECTURE.md   # Техническая архитектура
├── TROUBLESHOOTING.md # Решение проблем
└── API_EXAMPLES.json # Примеры API
```

---

## ⚡ Горячие клавиши

В окнах сервисов:
- `Ctrl+C` - Остановить сервис
- `Ctrl+Break` - Принудительная остановка

---

## 🔧 Минимальные требования

- **ОС:** Windows 10/11
- **ЦП:** 8+ ядер (рекомендуется)
- **ОЗУ:** 12 GB
- **Диск:** 15 GB свободного места
- **ПО:** Node.js 18+, Python 3.10+

---

## 📞 Поддержка

При проблемах:
1. Проверьте `TROUBLESHOOTING.md`
2. Посмотрите логи в окнах сервисов
3. Запустите `quick_test.py`

---

## ✅ Чек-лист готовности

- [ ] Установлены Node.js и Python
- [ ] Выполнен `install.bat` без ошибок
- [ ] Запущен `start_cluster.bat`
- [ ] Все 5 окон открылись
- [ ] `quick_test.py` прошел успешно
- [ ] API отвечает на запросы

**Готово! Кластер Tumaris работает! 🎉**
