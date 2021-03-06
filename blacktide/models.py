from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, DateTime, Integer, SmallInteger, Date, Time

DeclarativeBase = declarative_base()


def create_all_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class RaceMeta(DeclarativeBase):
    __tablename__ = "race_meta"

    race_id = Column(String, primary_key=True)
    race_name = Column(String)
    race_datetime = Column(DateTime)
    race_no = Column(SmallInteger)
    race_days = Column(SmallInteger)
    race_weeks = Column(SmallInteger)
    race_grade = Column(String)
    race_horses = Column(SmallInteger)

    track_meter = Column(SmallInteger)
    track_place = Column(String)
    track_rotation = Column(String)
    track_type = Column(String)
    track_side = Column(String)
    track_surface = Column(String)
    track_condition = Column(String)
    track_weather = Column(String)

    cond_intl = Column(String)
    cond_age = Column(String)
    cond_jockey = Column(String)
    cond_local = Column(String)
    cond_weight = Column(String)

    prize1 = Column(Integer)
    prize2 = Column(Integer)
    prize3 = Column(Integer)
    prize4 = Column(Integer)
    prize5 = Column(Integer)


class RacePayoff(DeclarativeBase):
    __tablename__ = "race_payoff"

    race_id = Column(String, primary_key=True)
    odds_id = Column(SmallInteger, primary_key=True)
    kind = Column(String)
    comb1 = Column(SmallInteger)
    comb2 = Column(SmallInteger)
    comb3 = Column(SmallInteger)
    yen = Column(Integer)
    popularity = Column(String)


class RaceResult(DeclarativeBase):
    __tablename__ = "race_result"

    race_id = Column(String, primary_key=True)
    row = Column(Integer, primary_key=True)
    race_datetime = Column(DateTime)
    fp = Column(String)
    bk = Column(Integer)
    pp = Column(Integer)
    horse_id = Column(String)
    horse_sex = Column(String)
    horse_age = Column(SmallInteger)
    jockey_id = Column(String)
    time = Column(Time)
    margin = Column(String)
    first_position = Column(SmallInteger)
    second_position = Column(SmallInteger)
    third_position = Column(SmallInteger)
    fourth_position = Column(SmallInteger)
    l3f = Column(Time)
    jockey_weight = Column(String)
    horse_weight = Column(String)
    fav = Column(String)
    odds = Column(String)
    blinker = Column(String)
    trainer_id = Column(String)


class Jockey(DeclarativeBase):
    __tablename__ = "jockeys"

    jockey_id = Column(String, primary_key=True)
    name = Column(String)
    kana = Column(String)


class Horse(DeclarativeBase):
    __tablename__ = "horses"

    horse_id = Column(String, primary_key=True)
    sex = Column(String)
    horse_name = Column(String)
    birthday = Column(Date)
    color = Column(String)
    trainer_id = Column(String)
    owner = Column(String)
    producer = Column(String)
    birthplace = Column(String)
    sire = Column(String)
    sire_sire = Column(String)
    sire_sire_sire = Column(String)
    sire_sire_mare = Column(String)
    sire_mare = Column(String)
    sire_mare_sire = Column(String)
    sire_mare_mare = Column(String)
    mare = Column(String)
    mare_sire = Column(String)
    mare_sire_sire = Column(String)
    mare_sire_mare = Column(String)
    mare_mare = Column(String)
    mare_mare_sire = Column(String)
    mare_mare_mare = Column(String)
