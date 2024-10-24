# Посібник з встановлення сервісу вручну

## Опис 
Цей посібник допоможе пройти процесс встановлення сервісу вручну. Для почтаку потрібно мати чисту систему Ubuntu, 
всі необхідні пакети та репозиторії будуть підключені пізніше.

## Загальні вимоги

- Python 3.10 !!!
- MariaDB 11+
- Ubuntu Server 20.04+
- Git

## Встановлення сервісу

### 1. Встановлення залежностей
Для початку потрібно встановити всі необхідні пакети. Виконайте наступні команди для встановлення Python 3.10 
і супутніх інструментів:

```bash
sudo apt-get update
sudo apt-get install -y curl libmariadb-dev gcc python3.10 python3.10-venv python3.10-dev git pkg-config
```
- Примітка: Якщо версія Python вище 3.10, сервіс працювати не буде. Інші пакети необхідні для коректної роботи з базою даних та репозиторієм.

### 2. Налаштуйте репозиторій MariaDB та встановіть СУБД MariaDB:
```bash
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo apt-get install -y mariadb-server libmysqlclient-dev libmariadb-dev
```

### 3. Запустіть СУБД MariaDB та налаштуйте атозапуск:
```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### 4. Створіть базу даних та користувача:
```bash
sudo mysql -e "CREATE DATABASE IF NOT EXISTS [DB_NAME] CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS '[DB_USER]'@'%' IDENTIFIED BY '[DB_PASSWORD]';"
sudo mysql -e "GRANT ALL PRIVILEGES ON [DB_NAME].* TO '[DB_USER]'@'%';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### 5. Клонуйте репозиторій:
```bash
git clone https://github.com/kshypachov/soap_sync_service.git
```

### 6. Перейдіть в папку з проектом:
```bash
cd soap_sync_service
```

### 7. Відредагуйте конфігураційні файли `alembic.ini` та `config.ini` додавши відомості про створену БД та користувача БД. 

### 8. Встановіть віртуалне середовище та активуйте його:
```bash
python3.10 -m venv soap_sync_service
source soap_sync_service/bin/activate
```

###  9. Встановіть залежності:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 10. Створіть структуру бд за допомогою alembic:
```bash
alembic revision --autogenerate -m "Init migration"
alembic upgrade head
```

### 11. Запустіть сервіс за допомогою команди:
```bash
python main.py
```