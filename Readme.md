
## Опис проєкту

Цей проєкт представляє собою сервіс на основі SOAP для управління даними про людей. Сервіс включає в себе створення, оновлення, видалення та отримання записів про людей в базі даних з використанням SQLAlchemy та Spyne.

## Структура проєкту

Проєкт складається з наступних файлів та директорій:

### Структура файлів і папок

```
project_root/
├── utils/
│   ├── validation.py
│   ├── update_person.py
│   ├── get_person.py
│   ├── delete_person.py
│   ├── create_peson.py
│   ├── config_utils.py
│   └── answer_structure.py
├── models/
│   ├── search.py
│   └── person.py
├── main.py
├── config.ini
├── alembic.ini
├── alembic/
└── Readme.md
```

### models

- `person.py`: Модель даних про людину з використанням SQLAlchemy та Spyne.
- `search.py`: Модель параметрів пошуку.

### utils

- `answer_structure.py`: Клас для структури відповіді.
- `config_utils.py`: Утиліти для роботи з конфігураційними файлами та логуванням.
- `create_person.py`: Логіка створення нової людини в базі даних.
- `delete_person.py`: Логіка видалення запису про людину за UNZR.
- `get_person.py`: Логіка отримання даних про людину за параметрами.
- `update_person.py`: Логіка оновлення даних про людину за UNZR.

## Встановлення

1. Клонуйте репозиторій:
    ```bash
    git clone <URL-репозиторію>
    ```
2. Встановіть залежності:
    ```bash
    pip install -r requirements.txt
    ```
3. Створіть файл конфігурації (наприклад, `config.ini`) з необхідними параметрами для підключення до бази даних та налаштування логування.

## Використання

### Запуск сервісу

1. Переконайтеся, що у вас налаштована база даних і файл конфігурації.
2. Запустіть сервіс:
    ```bash
    python main.py
    ```

### Приклади використання

- **Створення нової людини**
    ```python
    from utils.create_person import create_person
    from sqlalchemy.orm import sessionmaker
    from models.person import Base
    from sqlalchemy import create_engine
    from utils.config_utils import load_config, get_database_url

    config = load_config('config.ini')
    engine = create_engine(get_database_url(config))
    Session = sessionmaker(bind=engine)
    session = Session()

    person_data = {
        "name": "Тарас",
        "surname": "Шевченко",
        "patronym": "Григорович",
        "dateOfBirth": "1814-03-09",
        "gender": "male",
        "rnokpp": "1234567890",
        "passportNumber": "123456789",
        "unzr": "18140309-12345"
    }

    result = create_person(person_data, session)
    print(result.code, result.message)
    ```

- **Видалення людини за UNZR**
    ```python
    from utils.delete_person import delete_person_by_unzr

    result = delete_person_by_unzr("18140309-12345", session)
    print(result.code, result.message)
    ```

- **Отримання даних про людину за параметрами**
    ```python
    from utils.get_person import get_person_by_params_from_db

    search_params = {"name": "Тарас"}
    result = get_person_by_params_from_db(search_params, session)
    print(result.code, result.message)
    ```

- **Оновлення даних про людину**
    ```python
    from utils.update_person import update_person_by_unzr

    update_data = {
        "name": "Тарас",
        "surname": "Шевченко",
        "patronym": "Григорович",
        "dateOfBirth": "1814-03-09",
        "gender": "male",
        "rnokpp": "4444444444",
        "passportNumber": "111111111",
        "unzr": "18140309-12345"
    }

    result = update_person_by_unzr(update_data, session)
    print(result.code, result.message)
    ```

## Конфігурація

Приклад файлу конфігурації `config.ini`:

```ini
[database]
# тип бази даних (mysql, postgres тощо)
type = mysql
# хост бази даних
host = 10.0.20.242
# порт бази даних
port = 3306
# ім'я бази даних
name = soap
# ім'я користувача бази даних
username = soap
# пароль до бази даних
password = 1234

[logging]
# файл для запису логів
filename = /tmp/file.log
# режим роботи з файлом логів (a - додати, w - перезаписати)
filemode = a
# формат запису логів
format = %(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s
# формат дати і часу в логах
dateformat = %H:%M:%S
# рівень логування (DEBUG, INFO, WARNING, ERROR, CRITICAL)
level = DEBUG
```

### Опис параметрів конфігураційного файлу

- **[database]**
  - `type`: Тип бази даних, який використовується (наприклад, mysql, postgres).
  - `host`: Хост, на якому знаходиться база даних.
  - `port`: Порт для підключення до бази даних.
  - `name`: Назва бази даних.
  - `username`: Ім'я користувача для підключення до бази даних.
  - `password`: Пароль користувача для підключення до бази даних.

- **[logging]**
  - `filename`: Шлях до файлу, в який будуть записуватися логи.
  - `filemode`: Режим роботи з файлом логів (`a` - додавання до існуючого файлу, `w` - перезапис існуючого файлу).
  - `format`: Формат запису логів.
  - `dateformat`: Формат дати та часу в логах.
  - `level`: Рівень логування (DEBUG, INFO, WARNING, ERROR, CRITICAL).

## Ліцензія

Цей проєкт ліцензовано під ліцензією MIT. Див. файл LICENSE для отримання детальної інформації.

## Залежності

- SQLAlchemy
- Spyne
- Інші залежності, зазначені в `requirements.txt`

---