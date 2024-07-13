import logging
from sqlalchemy import select, update
from models.person import PersonModel as Person
from utils.answer_structure import AnswerResult as Result
import utils.config_utils

logger = logging.getLogger(__name__)


def update_person_by_unzr(person: dict, db_session) -> Result:
    """
    Оновлює запис про людину за UNZR.

    :param person: Дані про людину, які потрібно оновити.
    :param db_session: Сесія бази даних.
    :return: Результат операції у вигляді об'єкта Result.
    """
    # Логування запиту на оновлення даних
    logger.info(f"Отримано запит на оновлення даних для UNZR: {person}")

    # Створюємо запит на пошук запису за UNZR
    query = select(Person.id).where(Person.unzr == person.get("unzr"))

    try:
        # Виконуємо запит на пошук запису
        existing_person_id = db_session.execute(query).scalar_one_or_none()

        # Перевіряємо, чи знайдений запис
        if not existing_person_id:
            logger.warning(f"Запис з UNZR: {person.get('unzr')} не знайдено")
            return Result(Result.error, f"Запис з UNZR: {person.get('unzr')} не знайдено")

        # Створення запиту на оновлення даних
        update_query = (
            update(Person)
            .where(Person.id == existing_person_id)
            .values(**person)
        )

        # Виконуємо запит на оновлення даних
        db_session.execute(update_query)
        # Підтверджуємо зміни у базі даних
        db_session.commit()
        logger.info(f"Дані для UNZR: {person.get('unzr')} оновлено успішно")
        return Result(Result.success, f"Дані для UNZR: {person.get('unzr')} оновлено успішно")

    except Exception as e:
        # Відкочуємо зміни у разі помилки
        db_session.rollback()
        logger.error(f"Помилка під час оновлення даних: {e}")
        return Result(Result.error, "Помилка під час оновлення даних!")