import logging
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.complex import ComplexModel
from spyne.model.primitive import String
from spyne.model.fault import Fault
import models.person
import models.search
import utils.config_utils
import utils.get_person
import utils.validation
import utils.delete_person
import utils.update_person
import utils.create_peson
import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    conf_obj = utils.config_utils.load_config('config.ini')
    # Налаштовуємо логування
    utils.config_utils.configure_logging(conf_obj)
    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded")
    # Отримуємо URL бази даних
    SQLALCHEMY_DATABASE_URL = utils.config_utils.get_database_url(conf_obj)
except ValueError as e:
    logging.critical(f"Failed to load configuration: {e}")
    exit(1)

# створюємо об'єкт database, який буде використовуватися для виконання запитів

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

#people = {}
from datetime import datetime
class PersonService(ServiceBase):
    @rpc(models.search.SearchParams, _returns=Iterable(models.person.SpynePersonModel))
    def get_person_by_parameter(ctx, params):
        print(params)
        params_dict = {params.key: params.value}

        try:
            utils.validation.validate_parameter(params.key, params.value, models.person.SpynePersonModel)
            result = utils.get_person.get_person_by_params_from_db(params_dict, db_session)
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))

        # Преобразуем результат в список объектов SpynePersonModel
        persons = [
            models.person.SpynePersonModel(
                #id=row.id,
                name=row.name,
                surname=row.surname,
                patronym=row.patronym,
                dateOfBirth=row.dateOfBirth,
                gender=row.gender,
                rnokpp=row.rnokpp,
                passportNumber=row.passportNumber,
                unzr=row.unzr
            ) for row in result
        ]
        return persons

    @rpc(Unicode, _returns=Unicode)
    def delete_person_by_unzr(ctx, unzr):
        try:
            utils.validation.validate_parameter("unzr", unzr, models.person.SpynePersonModel)
            utils.delete_person.delete_person_by_rnokpp(unzr, db_session)
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))
        return f"Person with UNZR: {unzr} is deleted"

    @rpc(models.person.SpynePersonModel, _returns=Unicode)
    def edit_person(ctx, person):
        #Валидация пришедших данных
        models.person.SpynePersonModel.validate(person)

        person_dict = person.__dict__.copy()

        try:
            result_str, rowcount = utils.update_person.update_person_by_unzr(person_dict, db_session)
            return result_str
        except Exception as e:
            return e

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
            logger.info(f"Сталась помилка підчас обродки запиту на створення запису у базі даних: {e}")
            raise Fault(faultcode="Server", faultstring="Error")


application = Application([PersonService],
    tns='spyne.examples.person',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    # Включаем логирование для SQLAlchemy
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    server = make_server('127.0.0.1', 8000, wsgi_application)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/?wsdl")

    server.serve_forever()