from flask import Flask, render_template, request, jsonify
from weather import get_current_weather, get_forecast
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    try:
        current = get_current_weather(city)
        forecast = get_forecast(city)
        return jsonify({"current": current, "forecast": forecast})

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": f"City '{city}' not found. Check the spelling and try again."}), 404
        elif e.response.status_code == 401:
            return jsonify({"error": "Invalid API key. Check your .env file."}), 401
        else:
            return jsonify({"error": "An error occurred fetching weather data."}), 500

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "No internet connection. Please check your network."}), 503

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try again later."}), 504


if __name__ == "__main__":
    app.run(debug=True)
