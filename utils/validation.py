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
    logger.info(f"Validating parameter '{param_name}' with value '{param_value}'")

    if not hasattr(validation_model, param_name):
        logger.error(f"Parameter '{param_name}' is not a valid field of SpynePersonModel")
        raise Fault(faultcode="Client", faultstring=f"Parameter '{param_name}' is not a valid field")

    # Валидация значений параметров
    field_info = getattr(validation_model, param_name)
    if isinstance(field_info, str):
        if not isinstance(param_value, str):
            raise Fault(faultcode="Client", faultstring=f"Parameter '{param_name}' must be a string")
        if len(param_value) < field_info.min_len or len(param_value) > field_info.max_len:
            raise Fault(faultcode="Client",
                        faultstring=f"Parameter '{param_name}' length must be between {field_info.min_len} and {field_info.max_len}")

        if hasattr(field_info, 'pattern'):
            if not re.match(field_info.pattern, param_value):
                raise Fault(faultcode="Client",
                            faultstring=f"Parameter '{param_name}' does not match the required pattern")

    if isinstance(field_info, int):
        if not isinstance(param_value, int):
            raise Fault(faultcode="Client", faultstring=f"Parameter '{param_name}' must be an integer")

    if isinstance(field_info, datetime):
        if not isinstance(param_value, datetime):
            raise Fault(faultcode="Client", faultstring=f"Parameter '{param_name}' must be a datetime")