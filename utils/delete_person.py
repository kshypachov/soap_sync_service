import logging
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models.person import PersonModel as Person
from utils.answer_structure import AnswerResult as Result

logger = logging.getLogger(__name__)

def delete_person_by_unzr(unzr: str, db_session: Session):
    """
    Видаляє запис про людину за UNZR.

    :param unzr: UNZR запису, який необхідно видалити.
    :param db_session: Сесія бази даних.
    :return: Результат операції у вигляді об'єкта Result.
    """

    logger.info(f"Отримано дані для видалення запису у базі даних з UNZR: {unzr}")

    # Створюємо запит на видалення даних
    query = delete(Person).where(Person.unzr == unzr)

    try:
        # Виконуємо запит на видалення
        result = db_session.execute(query)
        # Підтверджуємо зміни в базі даних
        db_session.commit()
        # Отримуємо кількість видалених записів
        deleted_count = result.rowcount
    except Exception as e:
        # Відкочуємо зміни у разі непередбаченої помилки
        db_session.rollback()
        logger.error(f"Непередбачена помилка при видаленні запису з UNZR: {unzr}. Помилка: {e}")
        return Result(Result.error, f"Сталась помилка при видаленні запису з UNZR: {unzr}")

    # Перевіряємо, чи було видалено хоч один запис
    if deleted_count == 0:
        logger.warning(f"Запис з UNZR {unzr} не знайдено")
        return Result(Result.error, f"Запис з UNZR: {unzr} не знайдено.")
    else:
        logger.info(f"Кількість видалених записів: {deleted_count}")
        return Result(Result.success, f"Успішно видалено {deleted_count} запис(ів) з UNZR {unzr}.")

