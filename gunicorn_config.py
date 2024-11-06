import utils.config_utils
import multiprocessing
import logging
import os



try:

    # Завантаження конфігурації
    conf_obj = utils.config_utils.load_config('config.ini')
    service_host = utils.config_utils.get_config_param(conf_obj, 'service', 'host_interface', 'SERVICE_HOST_INTERFACE', default='0.0.0.0')
    service_port = utils.config_utils.get_config_param(conf_obj, 'service', 'service_port', 'SERVICE_PORT_INTERFACE', default='8000')



    bind = f'{service_host}:{service_port}'
    workers = multiprocessing.cpu_count() * 2 + 1
    timeout = 120

    def post_fork(server, worker):
        try:
            if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
                utils.config_utils.configure_logging_gunicorn(None)
            else:
                config = utils.config_utils.load_config('config.ini')
                utils.config_utils.configure_logging_gunicorn(config)
        except ValueError as e:
            logging.critical(f"Failed to load configuration: {e}")
            exit(1)


except Exception as e:
    print(f"Error: {e}")
    exit(-1)
