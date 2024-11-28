from models.person import PersonModel as Person
from sqlalchemy import select, and_

import logging
from utils.answer_structure import AnswerResult as Result


logger = logging.getLogger(__name__)


def get_person_by_params_from_db(params: dict, db_session) -> Result:
    """
    Отримує запис про людину за параметрами.

    :param params: Параметри пошуку запису.
    :param db_session: Сесія бази даних.
    :return: Результат операції у вигляді об'єкта Result.
    """
    logger.info(f"Запит на отримання даних з параметрами: {params}")

    # Створюємо список умов для пошуку
    conditions = []
    for key, value in params.items():
        if hasattr(Person, key):
            column = getattr(Person, key)
            conditions.append(column == value)

    # Перевіряємо, чи надані параметри для пошуку
    if not conditions:
        logger.warning("Не надано жодного параметра для пошуку")
        return Result(Result.error, "Не надано жодного параметра для пошуку")

    # Створюємо запит до БД для отримання даних
    query = (
        select(
            Person.name,
            Person.surname,
            Person.patronym,
            Person.dateOfBirth,
            Person.gender,
            Person.rnokpp,
            Person.passportNumber,
            Person.unzr,
        )
        .select_from(Person)
        .where(and_(*conditions))
    )

    try:
        # Виконуємо запит на отримання даних
        result = db_session.execute(query).fetchall()

        # Перевіряємо, чи знайдені записи
        if not result:
            logger.warning(f"Запис з параметрами {params} не знайдено")
            return Result(Result.error, "Запис не знайдено")
        else:
            logger.info("Отримано дані наступного запису: %s", result)
            return Result(Result.success, result)

    except Exception as e:
        # Логування помилки під час виконання запиту
        logger.error(f"Помилка під час виконання запиту на отримання даних: {e}")
        raise e
