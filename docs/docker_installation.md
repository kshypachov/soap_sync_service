# Посібник зі збірки та запуску Docker контейнеру для SOAP сервісу

## Опис

Цей посібник допоможе розгорнути додаток у середовищі Docker

## Зміст

1. [Вимоги](#вимоги)
2. [Змінні оточення](#змінні-оточення)
3. [Як зібрати Docker-образ](#як-зібрати-docker-образ)
4. [Як створити базу даних для сервісу](#як-створити-базу-даних-для-сервісу)
4. [Як запустити контейнер](#як-запустити-контейнер)
5. [Перегляд логів](#перегляд-логів)
6. [Використання змінних оточення для конфігурації](#використання-змінних-оточення-для-конфігурації)
7. [Використання конфігураційного файлу](#використання-конфігураційного-файлу)

## Вимоги

- Docker версії 20.10 і вище
- Docker Compose (якщо планується використання)

## Змінні оточення

Додаток підтримує конфігурацію через змінні оточення. Ось основні параметри:

- `USE_ENV_CONFIG`: Керує використанням змінних оточення для конфігурації. Якщо встановлено в `true`, додаток використовує змінні оточення замість конфігураційного файлу.
- `DB_USER`: Ім'я користувача бази даних.
- `DB_PASSWORD`: Пароль для підключення до бази даних.
- `DB_HOST`: Адреса хоста бази даних.
- `DB_NAME`: Ім'я бази даних.
- `DB_TYPE`: Тип бази даних. (Зараз підтримується тільки тип `mysql`)
- `DB_PORT`: Порт бази даних. (За замовченням `3306` для `mysql`)
- `LOG_FILENAME`: Ім'я файлу для логування. Якщо передано порожнє значення, логи будуть виводитися в консоль (stdout).
- `LOG_LEVEL`: Рівень логування (наприклад, `info`, `debug`).
- `LOG_FILEMODE`: Режим роботи з логами (наприклад, `a` — додавання до існуючого файлу або `w` — перезапис).
- `SERVICE_HOST_INTERFACE`: Адреса інтерфейсу для роботи з сервісом. (За замовченням `0.0.0.0`) 
- `SERVICE_PORT_INTERFACE`: Порт на якому працює сервіс. (За замовченням `8000`)

## Як зібрати Docker-образ

Щоб зібрати Docker-образ, виконайте наступну команду в кореневій директорії проєкту:

```bash
docker build -t my-soap-app .
```

Ця команда створить Docker-образ з іменем `my-fastapi-app`, використовуючи Dockerfile, який знаходиться в поточній директорії.

## Як створити базу даних для сервісу
Хоча контейнер і має у своєму складі компонент alembic котрий може створювати структуру бази даних, але його запуск з контейнера не є зручним.
Саме тому пропонується створити базу даних та її структуру вручну.

Виконайте команди на сервері баз даних:
```bash
# Створення бази даних, якщо вона не існує
sudo mysql -e "CREATE DATABASE IF NOT EXISTS [DB_NAME] CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Створення користувача, якщо він не існує
sudo mysql -e "CREATE USER IF NOT EXISTS '[DB_USER]'@'%' IDENTIFIED BY '[DB_PASSWORD]';"

# Призначення всіх привілеїв користувачеві на базу даних
sudo mysql -e "GRANT ALL PRIVILEGES ON [DB_NAME].* TO '[DB_USER]'@'%';"

# Оновлення привілеїв
sudo mysql -e "FLUSH PRIVILEGES;"

# Створення структури таблиці `person`
sudo mysql -e "USE [DB_NAME]; CREATE TABLE IF NOT EXISTS \`person\` (
  \`id\` int(11) NOT NULL AUTO_INCREMENT,
  \`name\` varchar(128) DEFAULT NULL,
  \`surname\` varchar(128) DEFAULT NULL,
  \`patronym\` varchar(128) DEFAULT NULL,
  \`dateOfBirth\` date DEFAULT NULL,
  \`gender\` enum('male','female') DEFAULT NULL,
  \`rnokpp\` varchar(10) DEFAULT NULL,
  \`passportNumber\` varchar(9) DEFAULT NULL,
  \`unzr\` varchar(14) DEFAULT NULL,
  PRIMARY KEY (\`id\`),
  UNIQUE KEY \`unzr\` (\`unzr\`),
  UNIQUE KEY \`passportNumber\` (\`passportNumber\`),
  UNIQUE KEY \`rnokpp\` (\`rnokpp\`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
```
Ці команди створять базу даних необхідної структури. 

## Як запустити контейнер

Щоб запустити контейнер з додатком, виконайте команду:

```bash
docker run -it --rm -p 8000:8000 \
    -e USE_ENV_CONFIG=true \
    -e DB_USER=myuser \
    -e DB_PASSWORD=mypassword \
    -e DB_HOST=mydbhost \
    -e DB_NAME=mydatabase \
    -e DB_TYPE=mysql \
    -e DB_PORT=3306 \
    -e LOG_LEVEL=info \
    -e LOG_FILENAME="" \
    my-soap-app
```

- Прапор `-p 8000:8000` перенаправляє порт 8000 на локальній машині на порт 8000 всередині контейнера.
- Змінні оточення `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME` задають параметри для підключення до бази даних.
- Змінна `LOG_FILENAME=""` задає виведення логів у консоль (stdout).

### Запуск з конфігураційним файлом

Ви можете запускати додаток, використовуючи конфігураційний файл замість змінних оточення. Для цього додайте файл `config.ini` в директорію додатка та вкажіть шлях до нього:

```bash
docker run -it --rm -p 8000:8000 \
    -v $(pwd)/config.ini:/app/config.ini \
    my-soap-app
```

- Прапор `-v $(pwd)/config.ini:/app/config.ini` монтує локальний файл конфігурації в контейнер за шляхом `/app/config.ini`.

### Приклад конфігураційного файлу `config.ini`:

```ini
[database]
db_type = mysql
username = myuser
password = mypassword
host = mydbhost
name = mydatabase

[logging]
filename = /var/log/app.log
filemode = a
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
dateformat = %Y-%m-%d %H:%M:%S
level = info
```

## Перегляд логів

Якщо ви налаштовуєте виведення логів у консоль, ви можете переглядати їх за допомогою команди:

```bash
docker logs <container_id>
```

Якщо логи зберігаються у файл (через змінну `LOG_FILENAME` або конфігураційний файл), ви можете налаштувати монтування директорії з логами на локальній машині:

```bash
docker run -it --rm -p 8000:8000 \
    -e LOG_FILENAME="/var/log/app.log" \
    -v $(pwd)/logs:/var/log \
    my-soap-app
```

Тут `-v $(pwd)/logs:/var/log` монтує локальну директорію для збереження логів.

## Використання змінних оточення для конфігурації

Якщо ви хочете повністю покладатися на змінні оточення для конфігурації, переконайтеся, що `USE_ENV_CONFIG=true`. Наприклад:

```bash
docker run -it --rm -p 8000:8000 \
    -e USE_ENV_CONFIG=true \
    -e DB_USER=myuser \
    -e DB_PASSWORD=mypassword \
    -e DB_HOST=mydbhost \
    -e DB_NAME=mydatabase \
    -e DB_TYPE=mysql \
    -e DB_PORT=3306 \
    -e LOG_LEVEL=info \
    -e LOG_FILENAME="" \
    my-soap-app
```

## Використання конфігураційного файлу

Якщо змінна `USE_ENV_CONFIG` не задана або встановлена в `false`, додаток буде використовувати конфігураційний файл для налаштування. Переконайтеся, що файл доступний у контейнері, як показано в розділі "Запуск з конфігураційним файлом".
