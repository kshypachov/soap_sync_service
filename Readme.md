
## Опис проєкту
Цей проєкт входить в набір прикладів взаємодії з API шлюзу безпечного обміну системи Трембіта (ШБО), що демонструють технічні особливості розробки вебсервісів та вебклієнтів, сумісних з системою Трембіта. 
Цей проєкт представляє собою сервіс на основі SOAP для управління даними про людей. Сервіс включає в себе створення, оновлення, видалення та отримання записів про людей в базі даних з використанням SQLAlchemy та Spyne.

## Вимоги

- Python 3.10+
- MariaDB 11+
- Ubuntu Server 20.04
- Git


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

### Ручне встановлення

1. Встановіть необхідні пакети:
    ```bash
    sudo apt-get update
    sudo apt-get install -y curl libmariadb-dev gcc python3 python3-venv python3-dev git pkg-config
    ```
2. Налаштуйте репозиторій MariaDB та встановіть СУБД MariaDB:
    ```bash
   curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
   sudo apt-get install -y mariadb-server libmysqlclient-dev libmariadb-dev
   ```
3. Запустіть СУБД MariaDB та налаштуйте атозапуск:
    ```bash
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

4. Створіть базу даних та користувача:
   ```bash
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS [DB_NAME] CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    sudo mysql -e "CREATE USER IF NOT EXISTS '[DB_USER]'@'%' IDENTIFIED BY '[DB_PASSWORD]';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON [DB_NAME].* TO '[DB_USER]'@'%';"
    sudo mysql -e "FLUSH PRIVILEGES;"
   ```

5. Клонуйте репозиторій:
    ```bash
    git clone https://github.com/kshypachov/soap_sync_service.git
    ```
6. Перейдіть в папку з проектом:
   ```bash
   cd soap_sync_service
   ```
7. Відредагуйте конфігураційні файли `alembic.ini` та `config.ini` додавши відомості про створену БД та користувача БД. 
8. Встановіть віртуалне середовище та активуйте його:
   ```bash
    python3 -m venv soap_sync_service
    source soap_sync_service/bin/activate
   ```
9. Встановіть залежності:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
10. Створіть структуру бд за допомогою alembic:
    ```bash
    alembic revision --autogenerate -m "Init migration"
    alembic upgrade head
    ```
11. Запустіть сервіс за допомогою команди:
    ```bash
    python main.py
    ```

## Встановлення за допомогою скрипта deploy.sh

Ми додали скрипт `deploy.sh` для автоматизації процесу встановлення. Цей сценарій запустить додаток у однопоточному режимі за допомогою Python. Це простий варіант підходить для тестування та дуже детального дебагу
Скрипт виконує наступні кроки:
1. Встановлює системні залежності.
2. Клонує репозиторій.
3. Створює та активує віртуальне середовище.
4. Встановлює залежності Python.
5. Налаштовує конфігурацію бази даних.
6. Створює структуру бази даних за допомогою Alembic.
7. Створює `systemd` сервіс для запуску застосунку.

#### Використання скрипта deploy.sh

1. Завантажте та запустіть скрипт для клонування репозиторію, встановлення залежностей та налаштування сервісу:

    ```bash
    wget https://raw.githubusercontent.com/kshypachov/soap_sync_service/master/deploy.sh
    chmod +x deploy.sh
    ```

2. Відредагуйте скрипт `deploy.sh`, замінивши значення змінних `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST` та `DB_PORT` на ваші реальні дані.

3. Запустіть скрипт:

   ```bash
   ./deploy.sh
   ```
## Встановлення за допомогою скрипта deploy_by_gunicorn.sh
Ми додали скрипт `deploy_by_gunicorn.sh` для автоматизації процесу встановлення. 
Цей сценарій запустить додаток у багатопоточному режимі за допомогою WSGI серверу Gunicorn. 
Це сценарій більше підходить для сервісів Трембіти, та є значно продуктивнішим рішенням.
Скрипт виконує наступні кроки:
1. Встановлює системні залежності.
2. Клонує репозиторій.
3. Створює та активує віртуальне середовище.
4. Встановлює залежності Python.
5. Налаштовує конфігурацію бази даних.
6. Створює структуру бази даних за допомогою Alembic.
7. Створює `systemd` сервіс для запуску застосунку.

#### Використання скрипта deploy_by_gunicorn.sh

1. Завантажте та запустіть скрипт для клонування репозиторію, встановлення залежностей та налаштування сервісу:

    ```bash
    wget https://raw.githubusercontent.com/kshypachov/soap_sync_service/master/deploy_by_gunicorn.sh
    chmod +x deploy_by_gunicorn.sh
    ```

2. Відредагуйте скрипт `deploy_by_gunicorn.sh`, замінивши значення змінних `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST` та `DB_PORT` на ваші реальні дані.

3. Запустіть скрипт:

   ```bash
   ./deploy_by_gunicorn.sh
   ```

## Видалення

Для видалення сервісу та всіх пов'язаних компонентів використовуйте скрипт `remove.sh`.

### Використання скрипта видалення

Скрипт `remove.sh` зупинить та видалить сервіс, видалить базу даних та користувача, а також видалить проект та віртуальне середовище.

```bash
chmod +x remove.sh
./remove.sh
```

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