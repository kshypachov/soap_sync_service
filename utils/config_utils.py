import configparser
import os
import logging
from logging.handlers import RotatingFileHandler

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)


# функція для зчитування конфігураційного файлу
def load_config(file_path: str, defaults: dict = None) -> configparser.ConfigParser:
    config = configparser.ConfigParser(defaults=defaults, interpolation=None)

    # Перевіряємо USE_ENV_CONFIG, і якщо true, не зчитуємо файл конфігурації
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        logger.info("Skipping config file loading, using environment variables only.")
    else:
    # Зчитуємо конфігураційний файл тільки якщо USE_ENV_CONFIG не true
        if not config.read(file_path):
            logger.error(f"Configuration file {file_path} not found or is empty.")
            raise FileNotFoundError(f"Configuration file {file_path} not found or is empty.")

    return config


# функція для отримання значення параметрів з конфіг файлу чи змінних оточення за їх ім'ям
def get_config_param(config: configparser.ConfigParser, section: str, param: str, env_var: str = None, default: str = None) -> str:
    # Якщо використовуються тільки змінні оточення
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        env_value = os.getenv(env_var)
        if env_var and env_value is not None:
            return env_value
        else:
            return default  # Вертаємо default, якщо змінної оточення немає

    # Якщо використовується тільки конфігураційний файл
    if config.has_option(section, param):
        return config.get(section, param)
    else:
        logger.error(f"Missing required config parameter: [{section}] {param}")
        raise ValueError(f"Missing required config parameter: [{section}] {param}")


# функція для формування url строки для підключення до бд
def get_database_url(config: configparser.ConfigParser) -> str:
    db_user = get_config_param(config, 'database', 'username', 'DB_USER')
    db_password = get_config_param(config, 'database', 'password', 'DB_PASSWORD')
    db_host = get_config_param(config, 'database', 'host', 'DB_HOST')
    db_name = get_config_param(config, 'database', 'name', 'DB_NAME')
    db_type = get_config_param(config, 'database', 'type', 'DB_TYPE')
    db_port = get_config_param(config, 'database', 'port', 'DB_PORT')

    missing_params = []
    if db_user is None:
        missing_params.append("DB_USER")
    if db_password is None:
        missing_params.append("DB_PASSWORD")
    if db_host is None:
        missing_params.append("DB_HOST")
    if db_name is None:
        missing_params.append("DB_NAME")
    if db_type is None:
        missing_params.append("DB_TYPE")
    if db_port is None:
        missing_params.append("DB_PORT")

    if missing_params:
        missing_params_str = ", ".join(missing_params)
        logger.error(f"Не вистачає наступних параметрів для підключення до бази даних: {missing_params_str}")
        raise ValueError(f"Missing database connection parameters: {missing_params_str}")

    return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# функція для налаштування логування
def configure_logging(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename', 'LOG_FILENAME', default=None)
    log_filemode = get_config_param(config, 'logging', 'filemode', 'LOG_FILEMODE', default=None)
    log_format = get_config_param(config, 'logging', 'format', 'LOG_FORMAT', default=None)
    log_datefmt = get_config_param(config, 'logging', 'dateformat' , 'LOG_DATE_FORMAT', default=None)
    log_level = get_config_param(config, 'logging', 'level', 'LOG_LEVEL', default="info").upper()

    # Якщо log_filename пустий, то виводимо логи в консоль (stdout), це необхідно для Docker
    if not log_filename:
        log_filename = None

    level = getattr(logging, log_level, logging.DEBUG)
    logging.basicConfig(
        filename=log_filename,   # Якщо None, то логи будуть виводитись в stdout
        filemode=log_filemode,
        format=log_format,
        datefmt=log_datefmt,
        level=level
    )

    # Встановлення обраного рівня логування для усіх модулів
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(level)

# Копіювання налаштувань логування в усі логери проєкту
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

# Налаштування логування у випадку якщо використовується guvicorn
def configure_logging_gunicorn(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename', 'LOG_FILENAME', default=None)
    log_filemode = get_config_param(config, 'logging', 'filemode', 'LOG_FILEMODE', default=None)
    log_format = get_config_param(config, 'logging', 'format', 'LOG_FORMAT', default=None)
    log_datefmt = get_config_param(config, 'logging', 'dateformat', 'LOG_DATE_FORMAT', default=None)
    log_level = get_config_param(config, 'logging', 'level', 'LOG_LEVEL', default="info").upper()

    level = getattr(logging, log_level, logging.DEBUG)

    # Якщо log_filename пустий, то виводимо логи в консоль (stdout)
    if not log_filename:
        handler = logging.StreamHandler()  # Логируем в stdout
    else:
        # Створюемо обробник з ротацією логів
        handler = RotatingFileHandler(filename=log_filename, mode=log_filemode, maxBytes=100000000, backupCount=10)

    # Створюємо загальний обробник логів
    formatter = logging.Formatter(fmt=log_format, datefmt=log_datefmt)
    handler.setFormatter(formatter)

    # Застосовуємо налаштування до усіх логерів в проєкті
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.handlers.clear()
        logger.addHandler(handler)

    logger_obj = logging.getLogger(__name__)
    logger_obj.setLevel(level)
    logger_obj.info("Configuration loaded by Gunicorn")