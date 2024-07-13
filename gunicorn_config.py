import utils.config_utils

try:
    # Завантаження конфігурації
    conf_obj = utils.config_utils.load_config('config.ini')
    service_host = utils.config_utils.get_config_param(conf_obj, 'service', 'host_interface')
    service_port = utils.config_utils.get_config_param(conf_obj, 'service', 'service_port')

    bind = f'{service_host}:{service_port}'
    workers = 4
    timeout = 120

except Exception as e:
    print(f"Error: {e}")
    exit(-1)
