import utils.config_utils
import multiprocessing
import logging
from logging.handlers import RotatingFileHandler



try:

    # Завантаження конфігурації
    conf_obj = utils.config_utils.load_config('config.ini')
    service_host = utils.config_utils.get_config_param(conf_obj, 'service', 'host_interface')
    service_port = utils.config_utils.get_config_param(conf_obj, 'service', 'service_port')



    bind = f'{service_host}:{service_port}'
    workers = 4
    timeout = 120

    #accesslog = 'gunicorn_access.log'
    #errorlog = 'gunicorn_error.log'
    #loglevel = 'info'


    def post_fork(server, worker):
        try:
            config = utils.config_utils.load_config('config.ini')
            utils.config_utils.configure_logging_gunicorn(config)
        except ValueError as e:
            logging.critical(f"Failed to load configuration: {e}")
            exit(1)


except Exception as e:
    print(f"Error: {e}")
    exit(-1)
