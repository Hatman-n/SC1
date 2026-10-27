import requests
import os
from datetime import datetime, date

def f(lat, lon):
   #короче список списков прогназа
    api_key = os.getenv("WEATHER_API_KEY")
    url="https://api.openweathermap.org/data/2.5/forecast"
    params ={
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru' }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data=response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            raise Exception("Ошибка API: Неверный ключ.")
        elif response.status_code == 404:
            raise Exception("Ошибка API: Город не найден.")
        else:
            raise err

    eschednev_data={}
    
    for i in data['list']:
        dt_txt=i['dt_txt'] #2026-10-22 12:00:00
        dt_obj=datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
        day_str = dt_obj.strftime('%Y-%m-%d')
    
        today=date.today()
        forecast_date=dt_obj.date()

        
        #сегодня+3 дня
        if today<=forecast_date <=date.fromordinal(today.toordinal()+3):
            if day_str not in eschednev_data:
                eschednev_data[day_str] = {
                    'temps_min':[],
                    'temps_max':[],
                    'humidity':[],
                    'wind_speed':[],
                    'descriptions':[],
                    'noon_desc': None }
            
            day= eschednev_data[day_str]
            day['temps_min'].append(i['main']['temp_min'])
            day['temps_max'].append(i['main']['temp_max'])
            day['humidity'].append(i['main']['humidity'])
            day['wind_speed'].append(i['wind']['speed'])
            day['descriptions'].append(i['weather'][0]['description'])
            
            
            if 12 <= dt_obj.hour <= 15:#что бы усреднить, посмотрим тольо днем
                day['noon_desc'] = i['weather'][0]['description']



    list1=[]
    for day_str, stats in sorted(eschednev_data.items()):
        #не нашли описание днем, берем первое че есть
        desc = stats['noon_desc'] if stats['noon_desc'] else stats['descriptions'][0]
        
        list1.append({
            'date': datetime.strptime(day_str, '%Y-%m-%d').date(),
            'temp_min': round(min(stats['temps_min']), 1),
            'temp_max': round(max(stats['temps_max']), 1),
            'humidity': round(sum(stats['humidity']) / len(stats['humidity'])),
            'wind_speed': round(max(stats['wind_speed']), 1),
            'description': desc.capitalize()
        })
    return list1