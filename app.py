import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    api_key = os.environ.get("OPENWEATHER_API_KEY")

    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    if not api_key:
        return jsonify({"error": "Weather API key is not configured."}), 500

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10
        )
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Weather unavailable.")}), response.status_code

        return jsonify({
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"]
        })

    except requests.RequestException:
        return jsonify({"error": "Network error. Please try again."}), 503

if __name__ == "__main__":
    app.run(debug=True)
