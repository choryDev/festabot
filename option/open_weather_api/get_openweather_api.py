import requests
from datetime import datetime, timedelta
apiKey = "71508b562ba50b24ace19f1506858569"

def get_weekly_weather(placeXY):
    url = "http://api.openweathermap.org/data/2.5/onecall?lat="+str(placeXY['x'])+"&lon="+str(placeXY['y'])+"&units=metric&lang=kr&appid=" + apiKey

    r = requests.get(url)
    weeklyWeather = r.json()['daily'] #오늘 포함 8일간  저장, index = 0 ~ 7
    return weeklyWeather
