import logging
from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.fault import Fault
import models.person
import models.search
import utils.config_utils
import utils.get_person
import utils.validation
import utils.delete_person
import utils.update_person
import utils.create_peson
from utils.logging_headers import log_soap_headers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import event, text
# from sqlalchemy.exc import DisconnectionError, SQLAlchemyError


try:

    # Завантаження конфігурації
    conf_obj = utils.config_utils.load_config('config.ini')

    #utils.config_utils.configure_logging_gunicorn(conf_obj)

    service_host = utils.config_utils.get_config_param(conf_obj, 'service', 'host_interface')
    service_port = utils.config_utils.get_config_param(conf_obj, 'service', 'service_port')

    # Налаштовуємо логування
    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded")

    #utils.config_utils.copy_logger_settings(utils.config_utils.app_name)

    # Встановлення обраного рівня логування для усіх модулів
    for logger_name in logging.root.manager.loggerDict:
        pass

    # Отримуємо URL бази даних
    SQLALCHEMY_DATABASE_URL = utils.config_utils.get_database_url(conf_obj)

except ValueError as e:
    logging.critical(f"Failed to load configuration: {e}")
    exit(1)

# Створюємо об'єкт database, який буде використовуватися для виконання запитів
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)
db_session = Session()


class PersonService(ServiceBase):
    @rpc(models.search.SearchParams, _returns=Iterable(models.person.SpynePersonModel))
    def get_person_by_parameter(ctx, params):
        # Логування параметрів запиту
        logger.info("Запит на отримання даних з параметрами: %s", params)

        log_soap_headers(ctx)

        params_dict = {params.key: params.value}

        try:
            # Валідація параметрів запиту
            utils.validation.validate_parameter(params.key, params.value, models.person.SpynePersonModel)
            result = utils.get_person.get_person_by_params_from_db(params_dict, db_session)
        except Exception as e:
            logger.info(f"Сталась помилка під час обробки запиту на отримання даних з параметрами з бази даних: {e}")
            raise Fault(faultcode="Server", faultstring="Неочікувана помилка")

        # Перетворення результату в список об'єктів SpynePersonModel
        persons = [
            models.person.SpynePersonModel(
                name=row.name,
                surname=row.surname,
                patronym=row.patronym,
                dateOfBirth=row.dateOfBirth,
                gender=row.gender,
                rnokpp=row.rnokpp,
                passportNumber=row.passportNumber,
                unzr=row.unzr
            ) for row in result.message
        ]
        return persons

    @rpc(Unicode, _returns=Unicode)
    def delete_person_by_unzr(ctx, unzr):

        try:
            # Валідація UNZR
            utils.validation.validate_parameter("unzr", unzr, models.person.SpynePersonModel)
            result = utils.delete_person.delete_person_by_unzr(unzr, db_session)
            if result.code == 0:
                return result.message
            else:
                raise Fault(faultcode="Server", faultstring=result.message)

        except Fault as f:
            raise f  # Перехоплення та повторне підняття виключення Fault

        except Exception as e:
            logger.info(f"Сталась помилка під час обробки запиту на видалення запису у базі даних: {e}")
            raise Fault(faultcode="Server", faultstring="Неочікувана помилка")

    @rpc(models.person.SpynePersonModel, _returns=Unicode)
    def edit_person(ctx, person):
        # Валідація надісланих даних
        models.person.SpynePersonModel.validate(person)

        person_dict = person.__dict__.copy()

        try:
            result = utils.update_person.update_person_by_unzr(person_dict, db_session)
            if result.code == 0:
                return result.message
            else:
                raise Fault(faultcode="Server", faultstring=result.message)

        except Fault as f:
            raise f  # Перехоплення та повторне підняття виключення Fault

        except Exception as e:
            logger.info(f"Сталась помилка під час обробки запиту на оновлення запису у базі даних: {e}")
            raise Fault(faultcode="Server", faultstring="Неочікувана помилка")

    @rpc(models.person.SpynePersonModel, _returns=Unicode)
    def create_person(ctx, person):
        #Валидация пришедших данных
        models.person.SpynePersonModel.validate(person)

        person_dict = person.__dict__.copy()

        try:
            result = utils.create_peson.create_person(person_dict, db_session)
            if result.code == 0:
                return result.message
            else:
                raise Fault(faultcode="Server", faultstring=result.message)

        except Fault as f:
            raise f  # Перехватываем исключение Fault и сразу же его поднимаем

        except Exception as e:
            logger.info(f"Сталась помилка підчас обробки запиту на створення запису у базі даних: {e}")
            raise Fault(faultcode="Server", faultstring="Неочікувана помилка")


application = Application([PersonService],
                          tns='spyne.examples.person',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

wsgi_application = WsgiApplication(application)

#цей блок коду виконується тільки при запуску за допомогою Python, без Gunicorn чи Unicorn чи іншого веб-сервера
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    #Конфігуруємо логування згідно параметрів у файлі кофігураці config.ini
    utils.config_utils.configure_logging(conf_obj)

    #Налаштовуємо адресу та порт для сервера
    server = make_server(service_host, int(service_port), wsgi_application)
    logging.info(f"listening to http://{service_host}:{service_port}")
    logging.info(f"wsdl is at: http://{service_host}:{service_port}/?wsdl")

    #from logging_tree import printout
    #printout()
    #Старт сервера
    server.serve_forever()
