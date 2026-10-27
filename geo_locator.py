import requests
import os

def get_location():
    url = "https://ipinfo.io/json"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() #если стату быудет 200 = ошибка
        data =response.json()
        loc=data.get('loc') 
        city =data.get('city')
        
        if loc and city:
            lat, lon=map(float, loc.split(','))
            print(f"Автоматически определен город: {city}, Координаты: {lat}, {lon}")
            return {'city': city, 'lat': lat, 'lon': lon}
        else:
            raise ValueError("Неполные данные")
            
    except Exception as e:
        print(f"Ошибка автоматического определения: {e}")
        print("Используем спб...минусы?")
        fallback_city=os.getenv("GEO_API_FALLBACK_CITY", "Sankt-Petersburg")
        
        return get_coords_by_city_name(fallback_city)

def get_coords_by_city_name(city0):
    url= f"https://nominatim.openstreetmap.org/search?q={city0}&format=json&limit=1"
    headers={'User-Agent': 'WeatherLab/1.0'} #не забываем обязательно указывать User-Agent - 
    try:
        resp=requests.get(url, headers=headers, timeout=5)
        data=resp.json()
        if data:
            lat=float(data[0]['lat'])
            lon=float(data[0]['lon'])
            print(f"Резервный город: {city0}")
            return {'city': city0, 'lat': lat, 'lon': lon}
    except:
        pass

    # ну если совсем дау...
    return {'city': city0, 'lat': 59.9343, 'lon': 30.3351}