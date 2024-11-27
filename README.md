# VibeHub

VibeHub — это платформа для проведения и организации мероприятий, которая упрощает взаимодействие между организаторами и участниками.

## 📚 Функциональность

- Создание и управление мероприятиями.
- Регистрация и управление участниками.
- Возможность добавления файлов и вложений к мероприятиям.

## 🛠️ Используемые технологии

### Frontend:
- **HTML**, **CSS**, **JavaScript**: Создание удобного и привлекательного интерфейса для пользователей.

### Backend:
- **FastAPI**: Быстрый и производительный фреймворк для реализации API.
- **SQLAlchemy**: ORM для работы с базой данных.
- **Alembic**: Управление миграциями базы данных.
- **PostgreSQL**: Реляционная база данных.

## ⚙️ Установка и запуск

### Предварительные требования:
- Установленный Python 3.10+.
- Установленный PostgreSQL.

### Шаги для запуска:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Jeeeperss/InnoHackaton-CyberCherti-VibeHub.git
   cd InnoHackaton-CyberCherti-VibeHub
   ```

2. **Настройте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**
   - Создайте базу данных в PostgreSQL.

5. **Примените миграции:**
   ```bash
   alembic upgrade head
   ```

6. **Запустите сервер:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Откройте приложение в браузере:**
   По умолчанию сервер запустится на `http://127.0.0.1:8000`.

## 📁 Структура проекта

```plaintext
InnoHackaton-CyberCherti-VibeHub/
│
├── api/                          # Роуты приложения
│   ├── authentication/           # Аутентификация пользователей
│   │   └── routers/              # Роуты аутентификации
│   └── room/                     # Роуты для работы с комнатами
│
├── core/                         # Основная логика приложения
│   ├── authentication/           # Логика и модели аутентификации
│   │   ├── auth/                 # Настройки аутентификации
│   │   ├── models/               # Модели данных
│   │   ├── schemas/              # Схемы данных
│   │   └── tools/                # Утилиты аутентификации
│   ├── db/                       # Работа с базой данных
│   │   ├── base/                 # Базовые классы моделей
│   │   └── worker/               # Воркер базы данных
│   └── room/                     # Логика работы с комнатами
│       ├── models/               # Модели комнат и вложений
│       └── tools/                # Утилиты для работы с комнатами
│
├── helpers/                      # Утилиты для форматирования данных
├── migration/                    # Миграции базы данных
```

## 🚀 Планы на будущее

- Добавить более сложные механики взаимодействия участников.
- Реализовать интеграцию с мессенджерами для уведомлений.
- Улучшить пользовательский интерфейс.

## 🤝 Участники

- **Jeeeperss** — Backend Developer.
- **Foxerfob** — Frontend Developer.
- **VladDashVS** — Designer.
- **CyberCherti** — Fullstack Development Team.

## 📃 Лицензия

Этот проект распространяется под лицензией [MIT](LICENSE).
