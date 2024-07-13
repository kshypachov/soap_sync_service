import logging
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from models.person import PersonModel as Person
from utils.answer_structure import AnswerResult as Result
import utils.config_utils

logger = logging.getLogger(__name__)


def create_person(person_data: dict, db_session) -> Result:
    """
    Створює новий запис про людину в базі даних.

    :param person_data: Дані про людину, які потрібно додати до бази даних.
    :param db_session: Сесія бази даних.
    :return: Результат операції у вигляді об'єкта Result.
    """
    # Логування отриманих даних для створення запису
    logger.info(f"Отримано дані для створення запису у базі даних: {person_data}")

    # Створення запиту на додавання нового запису
    query = insert(Person).values(person_data)

    try:
        # Виконання запиту на додавання запису
        db_session.execute(query)
        # Підтвердження змін у базі даних
        db_session.commit()
        # Повернення успішного результату
        return Result(Result.success, "Новий запис у базі даних створено успішно.")

    except IntegrityError as e:
        # Відкочення змін у разі помилки цілісності
        db_session.rollback()
        # Логування помилки цілісності
        logger.error(f"Сталась помилка цілосності при додаванні нового запису у БД: {e}")
        # Повернення результату з помилкою цілісності
        return Result(Result.error, f"Сталась помилка цілосності при додаванні нового запису у бд: {e}")

    except Exception as e:
        # Відкочення змін у разі будь-якої іншої помилки
        db_session.rollback()
        # Логування помилки
        logger.error(f"Помилка під час створення запису у базі даних: {e}")
        # Повернення результату з загальною помилкою
        return Result(Result.error, f"Помилка при створенні запису у базі даних.")

