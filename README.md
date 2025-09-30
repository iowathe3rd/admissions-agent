# Admissions Agent ALT

OSS self-hosted Telegram bot for the university admissions committee.

The agent assists applicants 24/7, guides them through the document submission process, provides information about programs and tuition fees, and records all interactions.

## ✨ Features

- 🤖 **Telegram Bot Interface** - Intuitive menu-driven navigation
- 🧠 **RAG-Powered Q&A** - Context-aware answers using Google Gemini
- 📚 **Knowledge Base** - Programs, FAQs, documents, and application steps
- 🔍 **Semantic Search** - Find relevant information using ChromaDB
- 📊 **Interaction Logging** - Track all user conversations
- 🔄 **Auto Data Loading** - Automatic seed data initialization
- 🌐 **REST API** - Full API for external integrations
- 🐳 **Docker Support** - Easy deployment with Docker Compose

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Bot Framework**: aiogram
- **Database**: SQLite + SQLAlchemy (async)
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini 2.5 series
- **Embeddings**: Google Gemini Embeddings
- **Containerization**: Docker
- **Testing**: pytest + pytest-asyncio

## 🤖 LLM Models

This project uses the Google Gemini 2.5 series of models through the new `google/genai` Python SDK.

- **Default**: `gemini-2.5-flash` for most tasks
- **Complex cases**: `gemini-2.5-pro` 
- **Embeddings**: `gemini-embedding-001`

**SDK Documentation**: [google-genai on PyPI](https://pypi.org/project/google-genai/)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Poetry (для управления зависимостями)
- Docker & Docker Compose (опционально)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd admissions-agent
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

4. **Run with convenience script**
   ```bash
   # Full setup: ingest data + run API + bot
   python run.py full
   
   # Or step by step:
   python run.py ingest  # Index the data
   python run.py api     # Start API server
   python run.py bot     # Start Telegram bot
   ```

### Docker Deployment

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

2. **Build and run services**
   ```bash
   docker-compose up --build
   ```

The services will start in the following order:
1. `rag-ingest` - Indexes the seed data (runs once)
2. `api` - FastAPI server on port 8000
3. `bot` - Telegram bot

## 📋 Environment Configuration

Create a `.env` file with the following variables:

```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
GEMINI_API_KEY="your_gemini_api_key"
```

### Getting API Keys

1. **Telegram Bot Token**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command and follow instructions
   - Copy the provided token

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

## 🔧 Development

### Project Structure

```
src/
├── app/          # FastAPI application
│   ├── main.py   # API entry point
│   ├── models.py # Database models
│   ├── db.py     # Database configuration
│   └── routers/  # API routes
├── bot/          # Telegram bot
│   ├── runner.py # Bot entry point
│   ├── handlers.py # Message handlers
│   └── keyboards.py # Inline keyboards
├── rag/          # RAG system
│   ├── ingest.py # Data indexing
│   ├── retriever.py # Context retrieval
│   └── genai.py  # Gemini integration
├── data/seed/    # Initial data
└── tests/        # Test suite
```

### Available Commands

```bash
# Data management
python run.py ingest    # Index seed data into vector store

# Development
python run.py api       # Start API server (localhost:8000)
python run.py bot       # Start Telegram bot
python run.py test      # Run test suite
python run.py full      # Complete setup and run

# Code quality
poetry run ruff check   # Lint code
poetry run black .      # Format code
poetry run pytest      # Run tests
```

### Adding New Data

To add new knowledge to the bot:

1. **Edit seed files** in `src/data/seed/`:
   - `programs.json` - Educational programs
   - `faqs.json` - Frequently asked questions
   - `documents.json` - Required documents
   - `steps.json` - Application process steps

2. **Re-index the data**:
   ```bash
   python run.py ingest
   ```

## 🧪 Testing

The project includes comprehensive tests:

```bash
# Run all tests
python run.py test

# Run specific test files
poetry run pytest src/tests/test_api.py -v
poetry run pytest src/tests/test_rag.py -v
poetry run pytest src/tests/test_bot.py -v
```

### Test Coverage

- **API Tests**: FastAPI endpoints, database operations
- **RAG Tests**: Context retrieval, relevance filtering, hallucination prevention  
- **Bot Tests**: Message handlers, callback queries, error handling

## 📊 API Documentation

When the API is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /healthz` - Health check
- `GET /programs/` - List educational programs
- `GET /faqs/` - List FAQs
- `POST /search/rag` - RAG search (debug endpoint)

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use proper secrets management
2. **Database**: Consider PostgreSQL for production
3. **Monitoring**: Add logging and monitoring solutions
4. **Scaling**: Use multiple bot instances if needed
5. **Backup**: Regular database and vector store backups

### Example Production docker-compose

```yaml
version: '3.8'
services:
  app:
    image: admissions-agent:latest
    environment:
      - DATABASE_URL=postgresql://...
      - TELEGRAM_BOT_TOKEN=...
      - GEMINI_API_KEY=...
    restart: unless-stopped
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 📚 Документация

Полная документация проекта доступна в папке [`docs/`](./docs/):

- 🚀 [Быстрый старт](./docs/quick-start.md)
- ⚙️ [Установка и настройка](./docs/installation.md) 
- 🏗️ [Архитектура системы](./docs/architecture/overview.md)
- 💻 [Руководство разработчика](./docs/development/local-development.md)
- 🤖 [Компоненты системы](./docs/components/)
- 📊 [Управление данными](./docs/data/seed-data.md)
- ❓ [FAQ и решение проблем](./docs/troubleshooting/faq.md)

## 🆘 Support

For questions and support:
- Check the [comprehensive documentation](./docs/)
- Review the [FAQ section](./docs/troubleshooting/faq.md)
- Create an issue on GitHub
- Check the API documentation at `/docs` endpoint
