#!/bin/bash

# Конфігураційні змінні
PROJECT_DIR="soap_sync_service"
SERVICE_NAME="soap_sync_service"
VENV_DIR="venv"
CONFIG_FILE="config.ini"

# Функція для зчитування параметрів з config.ini
function get_config_value() {
    local section=$1
    local key=$2
    local config_file=$3
    local value=$(awk -F "=" '/\['"$section"'\]/{a=1}a==1&&$1~/'"$key"'/{gsub(/[ \t]+$/, "", $2); print $2; exit}' $config_file)
    echo $value
}

# Отримання параметрів бази даних з config.ini
DB_NAME=$(get_config_value "database" "name" $CONFIG_FILE)
DB_USER=$(get_config_value "database" "username" $CONFIG_FILE)
DB_PASSWORD=$(get_config_value "database" "password" $CONFIG_FILE)

# Зупинка та видалення сервісу
echo "Зупинка та видалення сервісу..."
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo rm /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload

# Видалення бази даних та користувача
echo "Видалення бази даних та користувача..."
sudo mysql -e "DROP DATABASE IF EXISTS $DB_NAME;"
sudo mysql -e "DROP USER IF EXISTS '$DB_USER'@'%';"

# Видалення проекту та віртуального середовища
echo "Видалення проекту та віртуального середовища..."
cd ..
rm -rf $PROJECT_DIR

echo "Видалення завершено! Сервіс та пов'язані компоненти були успішно видалені."
