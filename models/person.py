import sqlalchemy
from datetime import date, datetime
import re
from pydantic import BaseModel, Field, validator
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer as SqlAlchemyInteger, String as SqlAlchemyString, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

# SQLAlchemy модель для представления данных о человеке
Base = declarative_base()

class genderEnum(str, enum.Enum):
    male = "male"
    female = "female"

class PersonModel(Base):
    __tablename__ = 'person'
    id = Column(SqlAlchemyInteger, primary_key=True, autoincrement=True)
    name = Column(SqlAlchemyString(128))
    surname = Column(SqlAlchemyString(128))
    patronym = Column(SqlAlchemyString(128), nullable=True)
    dateOfBirth = Column(Date)
    gender = Column(sqlalchemy.Enum(genderEnum))
    rnokpp = Column(SqlAlchemyString(10))
    passportNumber = Column(SqlAlchemyString(9))
    unzr = Column(SqlAlchemyString(14))


# Pydantic модель для валидации данных о человеке
class PersonMainModel(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    surname: str = Field(min_length=1, max_length=128)
    patronym: str = Field(None, max_length=128)
    dateOfBirth: date
    gender: str
    rnokpp: str
    passportNumber: str
    unzr: str

    @validator('dateOfBirth')
    def validate_date_of_birth(cls, value):
        if value and value > date.today():
            raise ValueError('dateOfBirth cannot be in the future')
        return value

    @validator('name', 'surname', 'patronym')
    def validate_name(cls, value):
        if value and not all(char.isalpha() for char in value):
            raise ValueError('Names must contain only alphabetic characters without space')
        return value

    @validator('gender')
    def validate_gender(cls, value):
        if value and value not in ['male', 'female']:
            raise ValueError('Gender must be either "male" or "female"')
        return value

    @validator('rnokpp')
    def validate_rnokpp(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('RNOKPP must be a 10 digit number')
        return value

    @validator('passportNumber')
    def validate_pasport_num(cls, value):
        if value and (not value.isdigit() or len(value) != 9):
            raise ValueError('passportNum must be a 9 digit number')
        return value

    @validator('unzr')
    def validate_unzr(cls, value):
        # Перевірка формата
        if not re.match(r'^\d{8}-\d{5}$', value):
            raise ValueError('UNZR must be in the format YYYYMMDD-XXXXC')

        # Розділ на частини
        date_part, code_part = value.split('-')
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:])

        # Перевірка правильності дати
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError('Invalid date in UNZR')

        # Перевірка кода
        code = int(code_part[:4])
        if not (0 <= code <= 9999):
            raise ValueError('Code in UNZR must be in the range from 0000 to 9999')

        # Перевірка контрольної цифри
        control_digit = int(code_part[4])
        if not (0 <= control_digit <= 9):
            raise ValueError('Invalid control digit in UNZR')

        return value
