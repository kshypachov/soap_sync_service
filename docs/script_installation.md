## Встановлення за допомогою скрипта deploy.sh

## Опис 

Ми додали скрипт `deploy.sh` для автоматизації процесу встановлення. Цей сценарій запустить додаток у однопоточному режимі за допомогою Python. Це простий варіант підходить для тестування та дуже детального дебагу
Скрипт виконує наступні кроки:
1. Встановлює системні залежності.
2. Клонує репозиторій.
3. Створює та активує віртуальне середовище.
4. Встановлює залежності Python.
5. Налаштовує конфігурацію бази даних.
6. Створює структуру бази даних за допомогою Alembic.
7. Створює `systemd` сервіс для запуску застосунку.

### Додавання репозиторію для python3.10
Для роботи цього сервісу обовʼязковий пакет python3.10, як у вашому репозиторії він відсутній, можна використати сторонній репозиторій. 
Щоб його встановити. виконайте команди: 
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

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
   
4. Перевірте стан сервісу:
```bash
systemctl status soap_sync_service
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
   
4. Перевірте стан сервісу:
```bash
systemctl status soap_sync_service_guvicorn
```
#### Конфігурація сервісу

- Конфігурація сервісу зберігається у файлі `config.ini` :
- Опис полів `config.ini` :

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
