# Налаштування Nginx як Reverse Proxy на Ubuntu з підтримкою HTTPS (самопідписаний сертифікат)

## Опис проєкту
Цей проєкт спрямований на налаштування Nginx у режимі reverse proxy для перенаправлення запитів від клієнтів до SOAP сервісу.  
Nginx буде виступати посередником між клієнтом і сервісом. Для захисту трафіку буде використаний самопідписаний SSL сертифікат.

## Загальні передумови
Перед налаштуванням Nginx, переконайтеся, що на сервері встановлені наступні компоненти:
- Ubuntu (рекомендована версія 20.04 або вище)
- Встановлений Nginx (версія 1.18 або вище)
- Встановлений OpenSSL (для генерації SSL сертифікатів)

## Встановлення Nginx на Ubuntu

1. Оновіть список пакетів:
    ```bash
    sudo apt update
    ```
2. Встановіть Nginx:
    ```bash
    sudo apt install nginx
   ```
   ## Налаштування Nginx як Reverse Proxy

1. Перейдіть до директорії з конфігураціями:
    ```bash
    cd /etc/nginx/sites-available
    ```

2. Створіть новий файл конфігурації для REST сервісу. Наприклад, `rest_service`:
    ```bash
    sudo nano /etc/nginx/sites-available/rest_service
    ```
3. Додайте наступну конфігурацію для reverse proxy:
    ```nginx
    server {
        listen 80;
        server_name _;
        
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
        ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
4. Створіть символічне посилання на конфігурацію в папці `sites-enabled`:
    ```bash
    sudo ln -s /etc/nginx/sites-available/rest_service /etc/nginx/sites-enabled/
    ```   

5. Переконайтеся, що символічне посилання створено коректно:
    ```bash
    ls -l /etc/nginx/sites-enabled/
    ```

## Генерація самопідписаного SSL сертифіката

Згенеруйте SSL сертифікат і приватний ключ:
    ```bash
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
    ```

    Під час генерації вам буде запропоновано ввести деякі дані (наприклад, країну, організацію, домен). Для тестових цілей можете ввести будь-які значення.

## Перевірка конфігурації
Щоб переконатися, що конфігурація Nginx правильна, виконайте команду:
 ```bash
sudo nginx -t
 ```
Якщо конфігурація правильна, ви побачите повідомлення `syntax is ok та test is successful`.

## Перезапуск Nginx

Після внесення змін перезапустіть Nginx:
```bash
sudo systemctl restart nginx