import sqlalchemy
from datetime import date, datetime
import re
from sqlalchemy import create_engine, Column, Integer as SqlAlchemyInteger, String as SqlAlchemyString, Date
from sqlalchemy.ext.declarative import declarative_base
import enum
from utils.validation import TrSOARValidationERROR


# SQLAlchemy модель для представлення даних про людину
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


from spyne import ComplexModel, Integer, Date, Unicode, String

# Spyne модель для представлення даних про людину з валідацією
class SpynePersonModel(ComplexModel):
    #id = Integer
    name = Unicode(min_len=1, max_len=128)
    surname = Unicode(min_len=1, max_len=128)
    patronym = Unicode(max_len=128)
    dateOfBirth = Date
    gender = Unicode(values=['male', 'female'])
    rnokpp = Unicode(min_len=10, max_len=10)#, pattern='^\d{10}$')
    passportNumber = Unicode(min_len=9, max_len=9)#, pattern='^\d{9}$')
    unzr = Unicode(min_len=14, max_len=14)

    @classmethod
    def validate(cls, obj):
        errors = []

        # Валідація номера паспорта
        if obj.passportNumber:
            if not (obj.passportNumber.isdigit() or re.match(r'^[А-Я]{2} \d{6}$', obj.passportNumber)):
                errors.append(f'passportNubmer value {obj.passportNumber} is not valid, passportNum must be a 9 digit number or follow the format "AA 123456" with Cyrillic letters and 6 digits')

        # Валідацію коду РНОКПП
        if obj.rnokpp:
            if not obj.rnokpp.isdigit():
                errors.append(f'rnokpp value {obj.rnokpp} is not valid, rnokpp should contain only digits')

        # Валідація поля dateOfBirth
        if obj.dateOfBirth and obj.dateOfBirth > date.today():
            errors.append(f'dateOfBirth {obj.dateOfBirth} value is not valid, cannot be in the future')

        # Валідація поля name, surname и patronym
        for field in ['name', 'surname', 'patronym']:
            value = getattr(obj, field)
            if value and not all(char.isalpha() for char in value):
                errors.append(f'{field} must contain only alphabetic characters without space')

        # Валідація поля unzr
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

