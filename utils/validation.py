import logging
#from models.person import PersonGet
from typing import Any
from pydantic import BaseModel
from spyne.model.fault import Fault
from datetime import datetime

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

def validate_parameter_name(param_name: str, validation_model: Any):
    logger.info(f"Validating parameter '{param_name}")

    if not hasattr(validation_model, param_name):
        logger.error(f"Parameter '{param_name}' is not a valid field of {validation_model.__name__}")
        raise ValueError(f"Parameter '{param_name}' is not a valid field")


def validate_parameter(param_name: str, param_value: Any, validation_model: Any):
    logger.info(f"Validating parameter '{param_name}")

    if not hasattr(validation_model, param_name):
        logger.error(f"Parameter '{param_name}' is not a valid field of {validation_model.__name__}")
        raise ValueError(f"Parameter '{param_name}' is not a valid field")

    # Создаем временный объект модели
    temp_obj =validation_model()
    setattr(temp_obj, param_name, param_value)

    # Пробуем валидировать объект
    validation_model.validate(temp_obj)
    # try:
    #
    #     print(f"Validation of {param_name} passed!")
    # except Fault as e:
    #     print(f"Validation of {param_name} failed: {e}")
