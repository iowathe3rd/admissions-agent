# 📊 Seed данные

Руководство по управлению начальными данными для системы знаний Admissions Agent.

## Обзор seed данных

Seed данные - это начальная база знаний, которая индексируется в векторную базу данных для работы RAG системы. Все данные хранятся в JSON формате в папке `src/data/seed/`.

## Структура seed данных

```
src/data/seed/
├── programs.json         # Программы обучения
├── faqs.json            # Часто задаваемые вопросы
├── steps.json           # Шаги поступления
└── documents.json       # Необходимые документы
```

## Формат данных

### 1. Программы обучения (`programs.json`)

```json
[
  {
    "id": 1,
    "name": "Программная инженерия",
    "category": "bachelor",
    "description": "Подготовка специалистов в области разработки программного обеспечения, системного анализа и проектирования сложных информационных систем.",
    "duration": "4 года",
    "cost": "450000",
    "cost_currency": "RUB",
    "cost_period": "год",
    "degree": "Бакалавр",
    "form_of_study": "Очная",
    "language": "Русский",
    "requirements": [
      "ЕГЭ по математике (профильный уровень) - от 70 баллов",
      "ЕГЭ по русскому языку - от 70 баллов",
      "ЕГЭ по информатике и ИКТ - от 75 баллов"
    ],
    "subjects": [
      "Программирование",
      "Алгоритмы и структуры данных",
      "Базы данных",
      "Веб-разработка",
      "Мобильная разработка",
      "Тестирование ПО"
    ],
    "career_prospects": [
      "Программист",
      "Системный аналитик",
      "Архитектор ПО",
      "Team Lead",
      "Product Manager"
    ],
    "employment_rate": "95%",
    "average_salary": "150000",
    "partner_companies": [
      "Яндекс",
      "VK",
      "Сбербанк",
      "Тинькофф"
    ],
    "highlights": [
      "Практико-ориентированное обучение",
      "Стажировки в IT-компаниях",
      "Участие в реальных проектах",
      "Сильная математическая подготовка"
    ],
    "admission_committee_contacts": {
      "phone": "+7 (495) 123-45-67",
      "email": "admission@alt.university",
      "office": "Корпус А, аудитория 101"
    }
  }
]
```

### Поля программ

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `id` | number | ✅ | Уникальный идентификатор |
| `name` | string | ✅ | Название программы |
| `category` | string | ✅ | Категория: `bachelor`, `master`, `specialist` |
| `description` | string | ✅ | Подробное описание программы |
| `duration` | string | ✅ | Длительность обучения |
| `cost` | string | ✅ | Стоимость обучения |
| `cost_currency` | string | ⚪ | Валюта (по умолчанию RUB) |
| `cost_period` | string | ⚪ | Период оплаты (год, семестр) |
| `degree` | string | ⚪ | Получаемая степень |
| `form_of_study` | string | ⚪ | Форма обучения |
| `language` | string | ⚪ | Язык обучения |
| `requirements` | array | ⚪ | Требования для поступления |
| `subjects` | array | ⚪ | Изучаемые предметы |
| `career_prospects` | array | ⚪ | Карьерные перспективы |
| `employment_rate` | string | ⚪ | Процент трудоустройства |
| `average_salary` | string | ⚪ | Средняя зарплата выпускников |
| `partner_companies` | array | ⚪ | Компании-партнеры |
| `highlights` | array | ⚪ | Особенности программы |
| `admission_committee_contacts` | object | ⚪ | Контакты приёмной комиссии |

### 2. FAQ (`faqs.json`)

```json
[
  {
    "id": 1,
    "question": "Как подать документы на поступление?",
    "answer": "Документы можно подать несколькими способами:\n\n1. **Лично** в приёмной комиссии (корпус А, аудитория 101)\n2. **Онлайн** через личный кабинет на сайте university.alt\n3. **Почтой России** по адресу: 123456, Москва, ул. Университетская, 1\n\nНеобходимые документы:\n- Заявление о приёме\n- Документ об образовании (оригинал или копия)\n- Результаты ЕГЭ\n- Паспорт (копия)\n- Фотографии 3x4 (6 штук)\n\nПодача документов: с 20 июня по 25 июля.",
    "category": "admission",
    "keywords": [
      "подача документов",
      "поступление",
      "приёмная комиссия",
      "документы",
      "заявление"
    ],
    "priority": 1,
    "last_updated": "2024-01-15"
  }
]
```

### Поля FAQ

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `id` | number | ✅ | Уникальный идентификатор |
| `question` | string | ✅ | Текст вопроса |
| `answer` | string | ✅ | Подробный ответ |
| `category` | string | ⚪ | Категория: `admission`, `tuition`, `academic`, `life` |
| `keywords` | array | ⚪ | Ключевые слова для поиска |
| `priority` | number | ⚪ | Приоритет (1-5, где 1 - высший) |
| `last_updated` | string | ⚪ | Дата последнего обновления |

### 3. Шаги поступления (`steps.json`)

```json
[
  {
    "id": 1,
    "step_number": 1,
    "title": "Выбор программы обучения",
    "description": "Изучите доступные программы обучения, их требования и особенности. Сравните программы по направлениям, стоимости и карьерным перспективам.",
    "category": "preparation",
    "duration": "1-2 недели",
    "required_documents": [],
    "helpful_links": [
      "https://alt.university/programs",
      "https://alt.university/admission-guide"
    ],
    "tips": [
      "Посетите дни открытых дверей",
      "Пообщайтесь с текущими студентами",
      "Изучите учебные планы программ"
    ],
    "common_mistakes": [
      "Выбор программы только по названию",
      "Игнорирование требований к ЕГЭ",
      "Невнимание к форме обучения"
    ],
    "deadline": null,
    "next_steps": [2]
  }
]
```

### Поля шагов

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `id` | number | ✅ | Уникальный идентификатор |
| `step_number` | number | ✅ | Номер шага по порядку |
| `title` | string | ✅ | Название шага |
| `description` | string | ✅ | Подробное описание |
| `category` | string | ⚪ | Категория этапа |
| `duration` | string | ⚪ | Примерная длительность |
| `required_documents` | array | ⚪ | Необходимые документы |
| `helpful_links` | array | ⚪ | Полезные ссылки |
| `tips` | array | ⚪ | Советы и рекомендации |
| `common_mistakes` | array | ⚪ | Частые ошибки |
| `deadline` | string | ⚪ | Крайний срок (если есть) |
| `next_steps` | array | ⚪ | ID следующих шагов |

### 4. Документы (`documents.json`)

```json
[
  {
    "id": 1,
    "name": "Аттестат о среднем общем образовании",
    "description": "Оригинал или заверенная копия документа о полном среднем образовании с приложением с оценками.",
    "category": "education",
    "required_for": ["bachelor"],
    "format": "Оригинал или нотариально заверенная копия",
    "additional_info": "Документы об образовании, полученные за рубежом, должны быть признаны в РФ.",
    "where_to_get": "Выдается в школе после успешного завершения 11 классов",
    "valid_period": "Бессрочно",
    "alternatives": [
      "Диплом о начальном профессиональном образовании",
      "Диплом о среднем профессиональном образовании"
    ],
    "common_issues": [
      "Утеря документа - нужно восстанавливать в школе",
      "Документ на иностранном языке требует перевода и легализации"
    ]
  }
]
```

### Поля документов

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `id` | number | ✅ | Уникальный идентификатор |
| `name` | string | ✅ | Название документа |
| `description` | string | ✅ | Подробное описание |
| `category` | string | ⚪ | Категория документа |
| `required_for` | array | ⚪ | Для каких программ требуется |
| `format` | string | ⚪ | Требуемый формат |
| `additional_info` | string | ⚪ | Дополнительная информация |
| `where_to_get` | string | ⚪ | Где получить документ |
| `valid_period` | string | ⚪ | Срок действия |
| `alternatives` | array | ⚪ | Альтернативные документы |
| `common_issues` | array | ⚪ | Частые проблемы |

## Категории и классификация

### Категории программ
- `bachelor` - Бакалавриат
- `master` - Магистратура  
- `specialist` - Специалитет
- `postgraduate` - Аспирантура

### Категории FAQ
- `admission` - Поступление
- `tuition` - Обучение
- `academic` - Академические вопросы
- `life` - Студенческая жизнь
- `career` - Карьера
- `financial` - Финансовые вопросы

### Категории шагов
- `preparation` - Подготовка
- `application` - Подача документов
- `examination` - Экзамены и испытания
- `enrollment` - Зачисление
- `start` - Начало обучения

### Категории документов
- `education` - Документы об образовании
- `identity` - Документы, удостоверяющие личность
- `military` - Военные документы
- `medical` - Медицинские документы
- `additional` - Дополнительные документы

## Лучшие практики

### Написание контента

1. **Ясность и простота**:
   - Используйте простые предложения
   - Избегайте сложной терминологии
   - Структурируйте информацию списками

2. **Полнота информации**:
   - Включайте все необходимые детали
   - Предвосхищайте вопросы пользователей
   - Добавляйте примеры

3. **Актуальность**:
   - Регулярно обновляйте данные
   - Указывайте даты изменений
   - Проверяйте ссылки

4. **SEO и поиск**:
   - Используйте ключевые слова
   - Добавляйте синонимы
   - Думайте как пользователь

### Структурирование данных

1. **Логическая группировка**:
   - Группируйте связанную информацию
   - Используйте иерархию
   - Избегайте дублирования

2. **Консистентность**:
   - Единый стиль написания
   - Одинаковые форматы дат
   - Единообразные термины

3. **Связи между данными**:
   - Используйте ID для связей
   - Избегайте циклических ссылок
   - Продумайте навигацию

## Процесс обновления данных

### 1. Подготовка изменений

```bash
# Создайте резервную копию
cp -r src/data/seed/ src/data/seed_backup_$(date +%Y%m%d)/

# Создайте ветку для изменений
git checkout -b update-seed-data
```

### 2. Редактирование файлов

Используйте любой JSON редактор или IDE. Рекомендуется VS Code с расширением JSON.

### 3. Валидация данных

```bash
# Проверьте валидность JSON
python -m json.tool src/data/seed/programs.json > /dev/null
python -m json.tool src/data/seed/faqs.json > /dev/null
python -m json.tool src/data/seed/steps.json > /dev/null
python -m json.tool src/data/seed/documents.json > /dev/null
```

### 4. Тестирование

```bash
# Переиндексируйте данные
python run.py ingest

# Протестируйте через бота
python run.py bot

# Проверьте через API
curl http://localhost:8000/programs/
```

### 5. Фиксация изменений

```bash
git add src/data/seed/
git commit -m "feat: update admission requirements for 2024"
git push origin update-seed-data
```

## Автоматизация

### Скрипт валидации

Создайте `scripts/validate_seed_data.py`:

```python
#!/usr/bin/env python3
"""Валидация seed данных."""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

def validate_json_file(file_path: Path) -> bool:
    """Проверяет валидность JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {file_path.name} - валидный JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {file_path.name} - ошибка JSON: {e}")
        return False

def validate_programs(data: List[Dict[str, Any]]) -> bool:
    """Валидирует данные программ."""
    required_fields = ['id', 'name', 'category', 'description']
    
    for program in data:
        for field in required_fields:
            if field not in program:
                print(f"❌ Программа {program.get('id', '?')}: отсутствует поле '{field}'")
                return False
    
    print(f"✅ Валидированы {len(data)} программ")
    return True

def main():
    """Основная функция валидации."""
    seed_dir = Path("src/data/seed")
    
    if not seed_dir.exists():
        print("❌ Папка src/data/seed не найдена")
        sys.exit(1)
    
    json_files = list(seed_dir.glob("*.json"))
    
    if not json_files:
        print("❌ JSON файлы не найдены")
        sys.exit(1)
    
    all_valid = True
    
    for json_file in json_files:
        if not validate_json_file(json_file):
            all_valid = False
            continue
        
        # Дополнительная валидация для каждого типа
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if json_file.name == "programs.json":
            if not validate_programs(data):
                all_valid = False
    
    if all_valid:
        print("\n✅ Все данные валидны!")
        sys.exit(0)
    else:
        print("\n❌ Найдены ошибки в данных!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Использование скрипта

```bash
python scripts/validate_seed_data.py
```

## Мониторинг качества данных

### Метрики качества

1. **Полнота данных**:
   - Процент заполненных обязательных полей
   - Наличие описаний для всех программ

2. **Актуальность**:
   - Дата последнего обновления
   - Проверка ссылок

3. **Консистентность**:
   - Единообразие форматов
   - Отсутствие дублей

### Автоматические проверки

```python
# Пример в CI/CD pipeline
def check_data_quality():
    """Проверяет качество данных."""
    
    with open('src/data/seed/programs.json') as f:
        programs = json.load(f)
    
    # Проверка на дубли
    ids = [p['id'] for p in programs]
    if len(ids) != len(set(ids)):
        raise ValueError("Найдены дублирующиеся ID программ")
    
    # Проверка обязательных полей
    for program in programs:
        if not program.get('description'):
            raise ValueError(f"Программа {program['id']} без описания")
```

## Миграция данных

### При изменении структуры

```python
#!/usr/bin/env python3
"""Миграция seed данных на новую схему."""

import json
from pathlib import Path

def migrate_programs_v1_to_v2():
    """Мигрирует программы с версии 1 на версию 2."""
    
    file_path = Path("src/data/seed/programs.json")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        programs = json.load(f)
    
    for program in programs:
        # Добавляем новые поля
        if 'cost_currency' not in program:
            program['cost_currency'] = 'RUB'
        
        if 'cost_period' not in program:
            program['cost_period'] = 'год'
        
        # Переименовываем поля
        if 'price' in program:
            program['cost'] = program.pop('price')
    
    # Сохраняем обновленные данные
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(programs, f, ensure_ascii=False, indent=2)
    
    print("Миграция завершена")

if __name__ == "__main__":
    migrate_programs_v1_to_v2()
```

Правильно структурированные seed данные - основа качественной работы RAG системы и пользовательского опыта.