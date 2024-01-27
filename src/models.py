from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from enum import Enum as BaseEnum

engine = create_engine('sqlite:///user_data.db')
Base = declarative_base()


class GenderEnum(BaseEnum):
    MALE = "Мужской"
    FEMALE = "Женский"


class WorkTypeEnum(BaseEnum):
    CHILD = "Ребенок"
    GOVERNMENT_JOB = "Государственная работа"
    UNEMPLOYED = "Не работал"
    CONFIDENTIAL = "Конфиденциально"
    SELF_EMPLOYED = "Самозанятый"


def get_worktypeenum_mapping():
    return {member.value: member for member in WorkTypeEnum}


class ResidenceTypeEnum(BaseEnum):
    RURAL = "Сельский"
    URBAN = "Городской"


class SmokingStatusEnum(BaseEnum):
    FORMER_SMOKER = "Раньше курил"
    NEVER_SMOKER = "Никогда не курил"
    CURRENT_SMOKER = "Курю"
    NOT_DISCLOSED = "Не скажу"


def create_enum_mapping(enum_class):
    enum_mapping = {}
    for member in enum_class:
        enum_mapping[member.value] = member
    return enum_mapping


work_type_mapping = create_enum_mapping(WorkTypeEnum)
residence_type_mapping = create_enum_mapping(ResidenceTypeEnum)
smoking_status_mapping = create_enum_mapping(SmokingStatusEnum)
gender_mapping = create_enum_mapping(GenderEnum)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    gender = Column(Enum(GenderEnum))
    age = Column(Integer)
    hypertension = Column(Boolean)
    heart_disease = Column(Boolean)
    ever_married = Column(Boolean)
    work_type = Column(Enum(WorkTypeEnum))
    residence_type = Column(Enum(ResidenceTypeEnum))
    avg_glucose_level = Column(Float)
    bmi = Column(Float)
    smoking_status = Column(Enum(SmokingStatusEnum))
    stroke = Column(Boolean)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
