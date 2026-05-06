import requests
from config import OPENWEATHER_API_KEY, DEFAULT_CITY

def get_weather(city: str = None) -> str:
    city = city or DEFAULT_CITY
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            temp        = round(data["main"]["temp"])
            feels_like  = round(data["main"]["feels_like"])
            humidity    = data["main"]["humidity"]
            description = data["weather"][0]["description"].capitalize()
            wind_speed  = round(data["wind"]["speed"] * 3.6)
            city_name   = data["name"]

            return (
                f"Current weather in {city_name}: {description}. "
                f"Temperature is {temp} degrees Celsius, feels like {feels_like}. "
                f"Humidity is {humidity} percent. "
                f"Wind speed is {wind_speed} kilometers per hour."
            )
        elif response.status_code == 401:
            return "Invalid OpenWeather API key. Please check config.py."
        elif response.status_code == 404:
            return f"City {city} not found. Please check the city name."
        else:
            return f"Weather service error: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "No internet connection. Cannot fetch weather."
    except Exception as e:
        return f"Weather error: {str(e)}"

def get_forecast(city: str = None) -> str:
    city = city or DEFAULT_CITY
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&cnt=3"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            result = f"3-hour forecast for {data['city']['name']}: "
            for item in data["list"]:
                time_str    = item["dt_txt"][11:16]
                temp        = round(item["main"]["temp"])
                description = item["weather"][0]["description"]
                result += f"At {time_str}, {description}, {temp} degrees. "
            return result
        else:
            return "Could not fetch forecast."

    except Exception as e:
        return f"Forecast error: {str(e)}"

def get_news() -> str:
    try:
        url = "https://feeds.bbcnews.com/news/rss.xml"
        response = requests.get(url, timeout=10)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        items = root.findall(".//item")[:5]
        headlines = []
        for item in items:
            title = item.find("title").text
            headlines.append(title)
        result = "Here are the latest BBC headlines. "
        for i, h in enumerate(headlines, 1):
            result += f"{i}. {h}. "
        return result
    except Exception as e:
        return f"News error: {str(e)}"

def handle_weather_command(command: str) -> str:
    cmd = command.lower()

    if "news" in cmd or "headlines" in cmd:
        return get_news()
    elif "forecast" in cmd:
        for word in cmd.split():
            if len(word) > 3 and word not in ["forecast", "weather", "what", "tell", "jarvis", "friday"]:
                return get_forecast(word)
        return get_forecast()
    else:
        for word in cmd.split():
            if len(word) > 3 and word not in ["weather", "temperature", "what", "tell", "jarvis", "friday", "like", "outside", "today"]:
                return get_weather(word)
        return get_weather()
