import logging
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models.person import PersonModel as Person

logger = logging.getLogger(__name__)

def delete_person_by_rnokpp(unzr: str, db_session: Session):
    """
    Удаляет запись о человеке по UNZR.

    :param unzr: UNZR записи, которую необходимо удалить.
    :param db_session: Сессия базы данных.
    :return: Количество удалённых записей.
    """
    # Создаём запрос на удаление данных
    query = delete(Person).where(Person.unzr == unzr)

    try:
        result = db_session.execute(query)
        db_session.commit()  # Подтверждаем изменения в базе данных
        deleted_count = result.rowcount  # Количество удалённых записей
    except Exception as e:
        db_session.rollback()  # Откатываем изменения в случае ошибки
        logger.error("Ошибка во время выполнения запроса на удаление: %s", e)
        raise ValueError("Ошибка удаления")

    try:
        if deleted_count == 0:
            logger.warning(f"Запись с UNZR {unzr} не найдена")
            raise ValueError("Person not found")

        logger.info(f"Количество удалённых записей: {deleted_count}")
        return deleted_count
    except Exception as e:
        logger.error("Ошибка во время выполнения запроса на удаление: %s", e)
        raise ValueError(e)