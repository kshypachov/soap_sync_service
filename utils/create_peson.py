import logging
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from models.person import PersonModel as Person
from answer_structure import AnswerResult as Result


logger = logging.getLogger(__name__)

def create_person(person_data: dict, db_session) -> Result:
    logger.info(f"Отримано дані для створення запису у базі даних: {person_data}")

    query = insert(Person).values(person_data)

    try:
        db_session.execute(query)
        db_session.commit()
        return Result(Result.success, "Новий запис у базі даних створено успішно.")

    except IntegrityError as e:
        db_session.rollback()
        logger.error(f"Сталась помилка цілосності при додаванні нового запису у бд: {e}")
        return Result(Result.error, f"Сталась помилка цілосності при додаванні нового запису у бд: {e}")

    except Exception as e:
        db_session.rollback()
        logger.error(f"Помилка під час створення запису у базі даних: {e}")
        raise ValueError(f"Failed to create person: {e}")