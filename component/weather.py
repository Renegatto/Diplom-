import requests

def get_weather_city(city = 'Minsk'):
    app_id = "94d8b74c4d0c302754e1af1f42419289"
    data = dict()
    weather = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}&units=metric'.format(app_id, city)).json()
    data['city'] = weather['name']
    data['temp'] = weather['main']['temp']
    data['temp_max'] = weather['main']['temp_max']
    data['temp_min'] = weather['main']['temp_min']
    data['humidity'] = weather['main']['humidity']
    data['pressure'] = weather['main']['pressure']
    return data
