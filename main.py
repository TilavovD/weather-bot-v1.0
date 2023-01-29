import requests
from datetime import datetime
import pytz
TZ = pytz.timezone("Asia/Tashkent")
response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Yangiyer?unitGroup=metric&key=74EU933EXL9R9L477YD9QUHHX&contentType=json")
data = response.json()
curr = data["currentConditions"]

time = curr["datetime"]
curr_temp = curr["temp"]
curr_feels_like = curr["feelslike"]
curr_humidity = curr["humidity"]
curr_conditions = curr["conditions"]

sunrise = curr["sunrise"]
sunset = curr["sunset"]
address = data["address"]
desc = data["description"]

today = data["days"][0]

date = today["datetime"]
tempmax = today["tempmax"]
tempmin = today["tempmin"]
humidity = today["humidity"]
wind_speed = today["windspeed"]


today_text = f"""Today: {date}
Address: {address}
Max temp: {tempmax}
Min temp: {tempmin}
Description: {desc}
Humidity: {humidity}
Wind speed: {wind_speed}

Sunrise: {sunrise}
Sunset: {sunset}
"""
current_text = f"""
Time as for: {time}
Time: {datetime.now(TZ)}
Temperature: {curr_temp}
Feels like: {curr_feels_like}
Conditions: {curr_conditions}
"""