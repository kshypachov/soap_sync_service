import configparser
import os
import logging
from logging.handlers import RotatingFileHandler

#app_name = "soap_service"

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

    level = getattr(logging, log_level, logging.DEBUG)
    logging.basicConfig(
        filename=log_filename,
        filemode=log_filemode,
        format=log_format,
        datefmt=log_datefmt,
        level=level
    )

    # Встановлення обраного рівня логування для усіх модулів
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(level)


def copy_logger_settings(source_logger_name):
    source_logger = logging.getLogger(source_logger_name)
    handlers = source_logger.handlers
    level = source_logger.level
    for logger_name in logging.root.manager.loggerDict:
        if logger_name != source_logger_name:
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)
            for handler in handlers:
                if not any(isinstance(h, type(handler)) for h in logger.handlers):
                    logger.addHandler(handler)


def configure_logging_gunicorn(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename')
    log_filemode = get_config_param(config, 'logging', 'filemode')
    log_format = get_config_param(config, 'logging', 'format')
    log_datefmt = get_config_param(config, 'logging', 'dateformat')
    log_level = get_config_param(config, 'logging', 'level').upper()

    level = getattr(logging, log_level, logging.DEBUG)

    # Создаем общий обработчик
    handler = RotatingFileHandler(filename=log_filename, mode=log_filemode, maxBytes=100000000, backupCount=10)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_datefmt)
    handler.setFormatter(formatter)

    # Применить настройки логирования ко всем логгерам
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.handlers.clear()  # Очищаем существующие обработчики
        logger.addHandler(handler)

    # Настроить основной логгер
    logger_obj = logging.getLogger(__name__)
    logger_obj.setLevel(level)
    logger_obj.info("Configuration loaded by Gunicorn")