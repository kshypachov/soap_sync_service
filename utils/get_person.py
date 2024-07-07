from models.person import PersonModel as Person
from sqlalchemy import select, and_, create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

def get_person_by_params_from_db(params: dict, db_session):
    logger.info("Запит на отримання даних з параметрами: %s", params)

    # Створюємо список умов для пошуку
    conditions = []
    for key, value in params.items():
        if hasattr(Person, key):
            column = getattr(Person, key)
            conditions.append(column == value)

    if not conditions:
        logger.warning("Не надано жодного параметра для пошуку")
        raise ValueError("No search parameters provided")

    # створюємо запит до БД для отримання даних
    query = (
        select(
            Person.id,
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
        person = db_session.execute(query).fetchall()

        if not person:
            logger.warning("Запис з параметрами %s не знайдено", params)
            raise ValueError("Person not found")

        logger.info("Отримано дані наступного запису: %s", person)
        return person

    except Exception as e:
        logger.error("Помилка під час виконання запиту на отримання даних: %s", e)
        raise ValueError(f"Failed to retrieve person: {e}")
