# 1. Base Image
FROM python:3.10-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION 1
ENV POETRY_VIRTUALENVS_CREATE false

# 3. Install Poetry
RUN pip install poetry

# 4. Set Workdir
WORKDIR /app

# 5. Copy dependency definitions
COPY pyproject.toml poetry.lock* ./

# 6. Install dependencies
RUN poetry install --no-dev --no-root

# 7. Copy the application code
COPY src/ ./src

# 8. Default command to run the bot
CMD ["poetry", "run", "python", "-m", "src.bot.runner"]
