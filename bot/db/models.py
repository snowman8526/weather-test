from aiogram.types import DateTime
from sqlalchemy import create_engine, Column, Integer, String, \
    ForeignKey, BigInteger, Boolean, Date, Numeric, \
    Text, func, TIMESTAMP

from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship

from datetime import datetime as dt

dbname = 'test'
user = 'postgres'
password = 'postgres'
host = '127.0.0.1'
engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{dbname}')


session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()
# engine = create_engine('sqlite:///example.db')


class UsersDb(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_telegram = Column(Integer)
    admin = Column(Boolean, default=False)
    city = Column(String)

class LogUser(Base):
    __tablename__ = 'log_user'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    command = Column(String)
    date = Column(TIMESTAMP, nullable=False, default=dt.utcnow)
    answer = Column(Text)
    user = relationship('UsersDb', foreign_keys='LogUser.id_user')


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_city = Column(Integer)
    temp = Column(Integer)
    perceived_temp = Column(Integer)  # температура окружающей среды по ощущенной
    description_weather = Column(String)
    humidity = Column(Integer)
    wind_speed = Column(Integer)
    date = Column(TIMESTAMP, nullable=False, default=dt.utcnow)

# class Point(Base):
#     __tablename__ = 'point'
#     id = Column(BigInteger, primary_key=True)
#     name = Column(String)
#     id_city = Column(Integer, ForeignKey('city.id'))
#     value = Column(Integer)
#     latitude = Column(Numeric)
#     longitude = Column(Numeric)
#     city = relationship('City', foreign_keys='Point.id_city')
#
#
# class DescriptionPoint(Base):
#     __tablename__ = 'description_point'
#     id = Column(Integer, primary_key=True)
#     id_point = Column(BigInteger, ForeignKey('point.id'))
#     id_telegram_file = Column(String)
#     description = Column(Text)
#     point = relationship('Point', foreign_keys='DescriptionPoint.id_point')
#
#
# class UserWeys(Base):
#     __tablename__ = 'user_weys'
#     id = Column(Integer, primary_key=True)
#     id_user = Column(Integer, ForeignKey('users.id'))
#     start_point_lat = Column(Numeric)
#     start_point_lon = Column(Numeric)
#     active = Column(Boolean, default=True)
#     users = relationship('UsersDb', foreign_keys='UserWeys.id_user')
#
#
# class NextPoint(Base):
#     __tablename__ = 'next_point'
#     id = Column(BigInteger, primary_key=True)
#     active = Column(Boolean, default=True)
#     do_not_reuse = Column(Boolean, default=False)
#     id_user_wey = Column(Integer, ForeignKey('user_weys.id'))
#     step = Column(Integer)
#     id_point = Column(BigInteger, ForeignKey('point.id'))
#     point = relationship('Point', foreign_keys='NextPoint.id_point')
#     user_weys = relationship('UserWeys', foreign_keys='NextPoint.id_user_wey')
#
#
# class NearbyPoint(Base):
#     __tablename__ = 'nearby_point'
#     id = Column(Integer, primary_key=True)
#     id_telegram = Column(Integer)
#     id_point = Column(BigInteger)
#     date = Column(Date, default=dt.today())
#     active = Column(Boolean, default=True)


Base.metadata.create_all(engine)
