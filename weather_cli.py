#!/usr/bin/env python3
"""
Weather CLI (OpenWeather)
Author: Hewad Rustom

Features:
- Get current weather by city name
- Metric units (°C) with conditions, humidity, wind
- Saves a local search history (weather_history.json)
- Reads API key from env var OPENWEATHER_API_KEY
"""

import os
import json
import time
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    raise SystemExit("Please install requests first: pip install requests")

API_BASE = "https://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "weather_history.json"


# -------------------- helpers --------------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"searches": []}


def save_history(db):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def get_api_key() -> Optional[str]:
    return os.environ.get("OPENWEATHER_API_KEY")


def fetch_weather(city: str, api_key: str):
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(API_BASE, params=params, timeout=10)
    if resp.status_code == 401:
        raise RuntimeError("Invalid or missing API key.")
    if resp.status_code == 404:
        raise RuntimeError("City not found.")
    resp.raise_for_status()
    return resp.json()


def render_weather(data: dict) -> str:
    name = data.get("name", "Unknown")
    sys = data.get("sys", {})
    country = sys.get("country", "")
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", [])
    desc = weather_list[0]["description"].title() if weather_list else "N/A"

    temp = main.get("temp")
    feels = main.get("feels_like")
    hum = main.get("humidity")
    wind_speed = wind.get("speed")

    return (
        f"\n🌦️  Weather — {name}, {country}\n"
        f"   • Temp: {temp:.1f}°C (feels {feels:.1f}°C)\n"
        f"   • Condition: {desc}\n"
        f"   • Humidity: {hum}%\n"
        f"   • Wind: {wind_speed} m/s\n"
    )


def add_to_history(db: dict, city: str, summary: str):
    db["searches"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "city": city,
        "summary": summary.replace("\n", " ").strip()
    })
    # keep last 20 only
    db["searches"] = db["searches"][-20:]
    save_history(db)


def show_history(db: dict, count: int = 5):
    if not db["searches"]:
        print("\n(No history yet.)")
        return
    print("\n🕘 Last searches:")
    for row in db["searches"][-count:][::-1]:
        print(f" - {row['time']}: {row['city']} — {row['summary']}")


# -------------------- cli --------------------
def menu() -> str:
    print("\n=== Weather CLI ===")
    print("1) Current weather by city")
    print("2) View last 5 searches")
    print("0) Exit")
    return input("Choose: ").strip()


def main():
    print("Welcome to Weather CLI (OpenWeather)")
    api_key = get_api_key()
    if not api_key:
        print("⚠️  OPENWEATHER_API_KEY environment variable is not set.")
        print("    Get a free API key at https://openweathermap.org/ and set it like:")
        print("    Windows (PowerShell):   setx OPENWEATHER_API_KEY your_key_here")
        print("    macOS/Linux (bash/zsh): export OPENWEATHER_API_KEY=your_key_here")
        return

    db = load_history()

    while True:
        choice = menu()
        if choice == "1":
            city = input("Enter city (e.g., London): ").strip()
            if not city:
                print("Please enter a city name.")
                continue
            try:
                data = fetch_weather(city, api_key)
                out = render_weather(data)
                print(out)
                # save compact summary for history
                main = data.get("main", {})
                weather_list = data.get("weather", [])
                desc = weather_list[0]["description"].title() if weather_list else "N/A"
                temp = main.get("temp")
                add_to_history(db, city, f"{temp:.1f}°C, {desc}")
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(0.5)
        elif choice == "2":
            show_history(db, 5)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
