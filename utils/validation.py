import logging
from typing import Any
import utils.config_utils

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

class TrSOARValidationERROR(Exception):
    pass

# функція для валідації назви параметра
def validate_parameter_name(param_name: str, validation_model: Any):
    logger.info(f"Validating parameter '{param_name}")

    # Перевірка, чи є параметр допустимим полем моделі валідації
    if not hasattr(validation_model, param_name):
        logger.error(f"Parameter '{param_name}' is not a valid field of {validation_model.__name__}")
        raise TrSOARValidationERROR(f"Parameter '{param_name}' is not a valid field")


# функція для валідації значення параметра
def validate_parameter(param_name: str, param_value: Any, validation_model: Any):
    logger.info(f"Validating parameter '{param_name}")

    # Перевірка, чи є параметр допустимим полем моделі валідації
    if not hasattr(validation_model, param_name):
        logger.error(f"Parameter '{param_name}' is not a valid field of {validation_model.__name__}")
        raise TrSOARValidationERROR(f"Parameter '{param_name}' is not a valid field")

    # Створення тимчасового об'єкта моделі для валідації значення параметра
    temp_obj =validation_model()
    setattr(temp_obj, param_name, param_value)
    try:
        # Спроба валідації об'єкта
        validation_model.validate(temp_obj)
    except Exception as e:
        raise TrSOARValidationERROR(f"Parameter '{param_name}' has an invalid value: {e}")

