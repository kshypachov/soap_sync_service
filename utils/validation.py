import logging
from typing import Any

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

