import os #для работы с ОСочкой, удобно для файликов
from dotenv import load_dotenv 
from geo_locator import get_location
from weather_client import f
from db_models import sozdanie_db, get_session, Moodel
from exporter import TOmarkdown
from datetime import datetime, date
load_dotenv()

sozdanie_db()
print("Создали бд")
print("Локация..")
try:
    location=get_location()
    city =location['city']
    lat =location['lat']
    lon = location['lon']
except Exception as e:
    print(f"Неверно указана локация")
    exit()
print("Прогнозы....")
try:
    print(f"Запрос прогноза для {city}...")
    Forecasts=f(lat, lon)
    print(f"Получено данных на {len(Forecasts)} дней.")
except Exception as e:
    print(f"Ошибка получения погоды: {e}")
    exit()

sessio=get_session()
saved=0

for day_data in Forecasts:
    #проверим есть ли уже эта запиь исключая...поворения, вспомни умное слово!!
    exists=sessio.query(Moodel).filter_by(
        city=city, 
        forecast_date=day_data['date']
    ).first()
    
    if not exists:
        zapis= Moodel(
            city=city,
            forecast_date=day_data['date'],
            temp_min=day_data['temp_min'],
            temp_max=day_data['temp_max'],
            humidity=day_data['humidity'],
            wind_speed=day_data['wind_speed'],
            description=day_data['description'],
            created_at=datetime.now()
        )
        sessio.add(zapis)
        saved +=1
    else:
        print(f"Запись за {day_data['date']} уже существует")
        
sessio.commit()
sessio.close() 
print("Сохранено")
TOmarkdown(city)
print("Оке Оке Всё")

