import configparser
import os
import logging

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

# функція для зчитування конфігураційного файлу
def load_config(file_path: str, defaults: dict = None) -> configparser.ConfigParser:
    config = configparser.ConfigParser(defaults=defaults, interpolation=None)
    config.read(file_path)
    return config

# функція для отримання значення параметрів з конфіг файлу за їх ім'ям
def get_config_param(config: configparser.ConfigParser, section: str, param: str) -> str:
    if config.has_option(section, param):
        return config.get(section, param)
    else:
        logger.error(f"Missing required config parameter: [{section}] {param}")
        raise ValueError(f"Missing required config parameter: [{section}] {param}")

# функція для формування url строки для підключення до бд
def get_database_url(config: configparser.ConfigParser) -> str:
    db_user = get_config_param(config, 'database', 'username')
    db_password = get_config_param(config, 'database', 'password')
    db_host = get_config_param(config, 'database', 'host')
    db_name = get_config_param(config, 'database', 'name')
    db_type = get_config_param(config, 'database', 'type')
    db_port = get_config_param(config, 'database', 'port')
    return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# функція для налаштування логування
def configure_logging(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename')
    log_filemode = get_config_param(config, 'logging', 'filemode')
    log_format = get_config_param(config, 'logging', 'format')
    log_datefmt = get_config_param(config, 'logging', 'dateformat')
    log_level = get_config_param(config, 'logging', 'level').upper()

    logging.basicConfig(
        filename=log_filename,
        filemode=log_filemode,
        format=log_format,
        datefmt=log_datefmt,
        level=getattr(logging, log_level, logging.DEBUG)
    )