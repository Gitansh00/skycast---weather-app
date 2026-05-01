# SkyCast — Python Weather App

A Flask web app that shows real-time weather and a 5-day forecast for any city, powered by the [OpenWeatherMap API](https://openweathermap.org/api).

## Features
- Current temperature, feels-like, humidity, wind speed, visibility, and pressure
- 5-day daily forecast with weather icons
- Clean, animated dark-themed UI
- Proper error handling (city not found, network errors, invalid API key)
- Unit tests with `unittest` and `unittest.mock`

## Project Structure
```
weather-app/
├── main.py              # Flask app & routes
├── weather.py           # API calls & data parsing
├── templates/
│   └── index.html       # Frontend UI
├── tests/
│   └── test_weather.py  # Unit tests
├── requirements.txt
├── .env                 # Your API key (never commit this!)
└── .env.example         # Safe template to share
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Gitansh00/skycast---weather-app.git
cd weather-app
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Get a free key at https://openweathermap.org/api (takes ~10 minutes to activate).

```bash
cp .env.example .env
# Edit .env and paste your key
```

### 5. Run the app
```bash
python main.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Run Tests
```bash
python -m pytest tests/ -v
# or
python -m unittest discover tests/
```

## Tech Stack
- **Backend**: Python 3.11+, Flask, Requests, python-dotenv
- **API**: OpenWeatherMap (free tier)
- **Frontend**: Vanilla HTML/CSS/JS (no framework needed)
- **Testing**: unittest, unittest.mock
