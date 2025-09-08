# 🌦️ Weather App (Python CLI)

A command-line weather app that fetches **live data** from OpenWeather and stores a **local search history** in `weather_history.json`.

## 🚀 Features
- Current weather by **city name**
- Metric units (°C) with **feels-like**, humidity, wind
- Saves your last 20 lookups to `weather_history.json`
- Simple **menu-driven** CLI

## 🛠️ Setup & Run
1) Get a free API key from **OpenWeather**: https://openweathermap.org/  
2) Set your API key as an environment variable named `OPENWEATHER_API_KEY`.

**Windows (PowerShell):**
```powershell
setx OPENWEATHER_API_KEY your_key_here

export OPENWEATHER_API_KEY=your_key_here

python weather_cli.py

Welcome to Weather CLI (OpenWeather)

=== Weather CLI ===
1) Current weather by city
2) View last 5 searches
0) Exit
Choose: 1
Enter city (e.g., London): Liverpool

🌦️  Weather — Liverpool, GB
   • Temp: 17.3°C (feels 16.1°C)
   • Condition: Broken Clouds
   • Humidity: 76%
   • Wind: 4.7 m/s

What I Learned

Consuming a public REST API with requests

Handling API keys via environment variables

Designing a clean CLI menu

Persisting simple data to JSON
