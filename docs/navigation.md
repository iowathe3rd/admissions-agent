# 📖 Навигация по документации

Быстрая навигация по всей документации проекта Admissions Agent.

## 🏗️ Для архитекторов

**Изучаете архитектуру?**
- 🏗️ [Обзор архитектуры](./architecture/overview.md) - Общая картина системы
- 📁 [Структура проекта](./architecture/project-structure.md) - Организация кода
- 🗄️ [База данных](./architecture/database.md) - Схема и модели
- 🧠 [RAG система](./architecture/rag.md) - AI и векторный поиск

**Развертываете в продакшн?**
- 🐳 [Docker развертывание](./deployment/docker.md) - Контейнеризация
- 🚀 [Продакшн конфигурация](./deployment/production.md) - Настройки для продакшна
- 📊 [Мониторинг](./deployment/monitoring.md) - Отслеживание системы

## 💻 Для разработчиков

**Начинаете разработку?**
- 💻 [Локальная разработка](./development/local-development.md) - Настройка IDE и workflow
- 📋 [Стандарты кодирования](./development/coding-standards.md) - Правила написания кода
- 🧪 [Тестирование](./development/testing.md) - Юнит и интеграционные тесты
- 🐛 [Отладка](./development/debugging.md) - Поиск и исправление ошибок

**Изучаете компоненты?**
- 🌐 [FastAPI Backend](./components/api.md) - REST API сервер
- 🤖 [Telegram Bot](./components/bot.md) - Интерфейс пользователя
- 🧠 [RAG & AI](./components/rag-ai.md) - Система ответов на вопросы
- 🗄️ [База данных](./components/database.md) - Хранение данных

## 📊 Для контент-менеджеров

**Управляете содержимым?**
- 📊 [Seed данные](./data/seed-data.md) - Структура и форматы данных
- 🔄 [Индексация](./data/indexing.md) - Обновление векторной базы
- ➕ [Добавление данных](./data/adding-data.md) - Новый контент

## 🔧 Для администраторов

**Администрируете систему?**
- 🤖 [Управление ботом](./admin/bot-management.md) - Настройки и команды
- 📝 [Логирование](./admin/logging.md) - Система логов
- 💾 [Резервное копирование](./admin/backup.md) - Бэкапы и восстановление

## 📚 API Reference

**Интегрируетесь с API?**
- 🌐 [REST API](./api/rest-api.md) - Полное описание эндпоинтов
- 📋 [Схемы данных](./api/schemas.md) - Модели запросов и ответов
- 💡 [Примеры запросов](./api/examples.md) - Готовые примеры

## 🎯 По задачам

### Хочу запустить систему
1. [Установка](./installation.md) → [Быстрый старт](./quick-start.md) → [Конфигурация](./configuration.md)

### Хочу понять как работает
1. [Обзор архитектуры](./architecture/overview.md) → [Компоненты](./components/) → [RAG система](./components/rag-ai.md)

### Хочу разрабатывать
1. [Локальная разработка](./development/local-development.md) → [Стандарты кода](./development/coding-standards.md) → [Тестирование](./development/testing.md)

### Хочу добавить данные
1. [Seed данные](./data/seed-data.md) → [Добавление данных](./data/adding-data.md) → [Индексация](./data/indexing.md)

### Хочу развернуть в продакшн
1. [Docker](./deployment/docker.md) → [Продакшн настройки](./deployment/production.md) → [Мониторинг](./deployment/monitoring.md)

### У меня проблема
1. [FAQ](./troubleshooting/faq.md) → [Решение проблем](./troubleshooting/common-issues.md) → GitHub Issues

## 📈 По уровню сложности

### 🟢 Начинающий уровень
- [Быстрый старт](./quick-start.md)
- [FAQ](./troubleshooting/faq.md)
- [Добавление данных](./data/adding-data.md)

### 🟡 Средний уровень
- [Архитектура](./architecture/overview.md)
- [Конфигурация](./configuration.md)
- [API документация](./api/rest-api.md)

### 🔴 Продвинутый уровень
- [Локальная разработка](./development/local-development.md)
- [RAG система](./components/rag-ai.md)
- [Продакшн развертывание](./deployment/production.md)

## 🔍 Поиск по документации

### По компонентам
- **Backend**: [API](./components/api.md), [База данных](./components/database.md)
- **Frontend**: [Telegram Bot](./components/bot.md)
- **AI**: [RAG система](./components/rag-ai.md)
- **Data**: [Seed данные](./data/seed-data.md), [Индексация](./data/indexing.md)

### По технологиям
- **Python**: [Локальная разработка](./development/local-development.md), [Стандарты кода](./development/coding-standards.md)
- **FastAPI**: [API компонент](./components/api.md), [REST API](./api/rest-api.md)
- **aiogram**: [Telegram Bot](./components/bot.md)
- **Docker**: [Docker развертывание](./deployment/docker.md)
- **Google Gemini**: [RAG & AI](./components/rag-ai.md)

### По типу задач
- **Установка**: [Установка](./installation.md), [Docker](./deployment/docker.md)
- **Настройка**: [Конфигурация](./configuration.md), [Продакшн](./deployment/production.md)
- **Разработка**: [Локальная разработка](./development/local-development.md), [Тестирование](./development/testing.md)
- **Отладка**: [FAQ](./troubleshooting/faq.md), [Решение проблем](./troubleshooting/common-issues.md)

## 📱 Мобильная навигация

Если вы читаете документацию на мобильном устройстве, рекомендуем начать с:

1. **📋 [FAQ](./troubleshooting/faq.md)** - самые частые вопросы
2. **🚀 [Быстрый старт](./quick-start.md)** - для первого запуска  
3. **📊 [Seed данные](./data/seed-data.md)** - для редактирования контента

## 🆘 Нужна помощь?

Если не нашли ответ в документации:

1. **Проверьте [FAQ](./troubleshooting/faq.md)** - 90% вопросов уже отвечены
2. **Изучите [решение проблем](./troubleshooting/common-issues.md)**
3. **Создайте issue на GitHub** с тегами и подробным описанием
4. **Обратитесь к команде разработки**

---
