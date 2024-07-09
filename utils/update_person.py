import logging
from sqlalchemy import select, update
from models.person import PersonModel as Person

logger = logging.getLogger(__name__)


def update_person_by_unzr(person: dict, db_session):
    logger.info("Запит на оновлення даних для UNZR: %s", person)

    # Створюємо запит на пошук запису за UNZR
    query = select(Person.id).where(Person.unzr == person.get("unzr"))

    try:
        existing_person_id = db_session.execute(query).scalar_one_or_none()

        if not existing_person_id:
            logger.warning("Запис з UNZR %s не знайдено", person.get("unzr"))
            raise ValueError("Person not found")

        # Створення запиту на оновлення даних
        update_query = (
            update(Person)
            .where(Person.id == existing_person_id)
            .values(**person)
        )

        result = db_session.execute(update_query)
        db_session.commit()

        if result.rowcount == 0:
            logger.info("Дані для UNZR %s не змінилися", person.get("unzr"))
            return f"Person with UNZR {person.get('unzr')} already up-to-date"
        else:
            logger.info("Дані для UNZR %s оновлено успішно", person.get("unzr"))
            return f"Person with UNZR {person.get('unzr')} updated successfully"

    except Exception as e:
        db_session.rollback()
        logger.error("Помилка під час оновлення даних: %s", e)
        raise ValueError(f"Failed to update person: {e}")


