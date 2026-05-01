import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city: str) -> dict:
    """Fetch current weather for a given city."""
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return parse_current_weather(data)


def get_forecast(city: str) -> list:
    """Fetch 5-day / 3-hour forecast for a given city."""
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 40,  # 5 days x 8 readings per day
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return parse_forecast(data)


def parse_current_weather(data: dict) -> dict:
    """Extract relevant fields from current weather API response."""
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "visibility": round(data.get("visibility", 0) / 1000, 1),  # m → km
        "pressure": data["main"]["pressure"],
    }


def parse_forecast(data: dict) -> list:
    """Extract one reading per day (noon) from the forecast response."""
    seen_dates = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        time = item["dt_txt"].split(" ")[1]
        # Prefer noon reading; otherwise take first available per day
        if date not in seen_dates or time == "12:00:00":
            seen_dates[date] = {
                "date": date,
                "temp_max": round(item["main"]["temp_max"]),
                "temp_min": round(item["main"]["temp_min"]),
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
            }
    return list(seen_dates.values())[:5]
