#модели для базы данных (блонды и брюнетки)
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime 
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL=os.getenv("DB_URL", "sqlite:///weather_lab.db")
en= create_engine(DATABASE_URL, echo=False) #управляет соединениями между///мост короче
b=declarative_base()#создаем базовый класс

class Moodel(b):
    __tablename__ = 'labka' #тока так, никак иначе:)
    id= Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)      
    forecast_date= Column(Date, nullable=False)
    temp_min = Column(Float)                     
    temp_max =Column(Float)                     
    humidity =Column(Integer)                   
    wind_speed= Column(Float)                  
    description = Column(String)                 
    created_at = Column(DateTime, default=datetime.now) 

def sozdanie_db():
    b.metadata.create_all(en)

def get_session():
    s=sessionmaker(bind=en)
    return s()