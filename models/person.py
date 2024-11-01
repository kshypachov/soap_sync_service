import sqlalchemy
from datetime import date, datetime
import re
#from pydantic import BaseModel, Field, validator
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.model.fault import Fault
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer as SqlAlchemyInteger, String as SqlAlchemyString, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from spyne.model.enum import Enum
import enum
from utils.validation import TrSOARValidationERROR

# SQLAlchemy модель для представления данных о человеке
Base = declarative_base()

class genderEnum(str, enum.Enum):
    male = "male"
    female = "female"
class PersonModel(Base):
    __tablename__ = 'person'
    id = Column(SqlAlchemyInteger, primary_key=True, autoincrement=True)
    name = Column(SqlAlchemyString(128), nullable=False)
    surname = Column(SqlAlchemyString(128), nullable=False)
    patronym = Column(SqlAlchemyString(128), nullable=True)
    dateOfBirth = Column(Date, nullable=False)
    gender = Column(sqlalchemy.Enum(genderEnum), nullable=False)
    rnokpp = Column(SqlAlchemyString(10), unique=True, nullable=False)
    passportNumber = Column(SqlAlchemyString(9), unique=True, nullable=False)
    unzr = Column(SqlAlchemyString(14), unique=True, nullable=False)


# Pydantic модель для валидации данных о человеке

from spyne import ComplexModel, Integer, Date, Unicode, String
# Spyne модель для представления данных о человеке с валидацией
class SpynePersonModel(ComplexModel):
    #id = Integer
    name = Unicode(min_len=1, max_len=128)
    surname = Unicode(min_len=1, max_len=128)
    patronym = Unicode(max_len=128)
    dateOfBirth = Date
    gender = Unicode(values=['male', 'female'])
    rnokpp = Unicode(min_len=10, max_len=10)#, pattern='^\d{10}$')
    passportNumber = Unicode(min_len=9, max_len=9)#, pattern='^\d{9}$')
    #unzr = Unicode(pattern=r'^\d{8}-\d{5}$')
    unzr = Unicode(min_len=14, max_len=14)

    @classmethod
    def validate(cls, obj):
        errors = []

        # Валидация поля dateOfBirth
        if obj.dateOfBirth and obj.dateOfBirth > date.today():
            errors.append('dateOfBirth cannot be in the future')

        # Валидация поля name, surname и patronym
        for field in ['name', 'surname', 'patronym']:
            value = getattr(obj, field)
            if value and not all(char.isalpha() for char in value):
                errors.append(f'{field} must contain only alphabetic characters without space')

        # Валидация поля unzr
        if obj.unzr:
            match = re.match(r'^\d{8}-\d{5}$', obj.unzr)
            if not match:
                errors.append('UNZR must be in the format YYYYMMDD-XXXXC')
            else:
                date_part, code_part = obj.unzr.split('-')
                year = int(date_part[:4])
                month = int(date_part[4:6])
                day = int(date_part[6:])
                try:
                    datetime(year, month, day)
                except ValueError:
                    errors.append('Invalid date in UNZR')
                code = int(code_part[:4])
                if not (0 <= code <= 9999):
                    errors.append('Code in UNZR must be in the range from 0000 to 9999')
                control_digit = int(code_part[4])
                if not (0 <= control_digit <= 9):
                    errors.append('Invalid control digit in UNZR')

        if errors:
            raise TrSOARValidationERROR(errors)

