import requests

def get_weather(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",  # Celsius
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather_main": data["weather"][0]["main"],
            "weather_description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "clouds": data["clouds"]["all"],
            "city": data["name"],
            "country": data["sys"]["country"],
        }
    else:
        return None