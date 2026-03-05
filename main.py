# main.py
import requests
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Voice input function
# -----------------------------
def get_city_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Please say your city name...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        city = recognizer.recognize_google(audio)
        print("✅ You said:", city)
        return city
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return None
    except sr.RequestError:
        print("❌ Could not connect to Google Speech Recognition.")
        return None

# -----------------------------
# Hybrid input: voice or type
# -----------------------------
def get_city():
    choice = input("Press Enter to type city or type 'v' for voice input: ").lower()
    if choice == "v":
        city = None
        while not city:
            city = get_city_voice()
    else:
        city = input("Enter city name: ")
    return city

# -----------------------------
# Weather fetch function
# -----------------------------
def get_weather(city):
    api_key = "c853f82afcff0566240f57b87488d8c3"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }
    return weather

# -----------------------------
# Outfit suggestion function
# -----------------------------
def suggest_outfit(temp, humidity, desc):
    outfit = ""
    if temp < 10:
        outfit = "Wear a heavy jacket and gloves."
    elif 10 <= temp < 20:
        outfit = "Wear a light jacket or sweater."
    elif 20 <= temp < 30:
        outfit = "Wear a T-shirt and jeans."
    else:
        outfit = "Wear cotton clothes and stay hydrated."

    if "rain" in desc.lower():
        outfit += " Carry an umbrella or wear a raincoat."
    if humidity > 80:
        outfit += " Use light and breathable fabrics."

    return outfit

# -----------------------------
# GUI display function
# -----------------------------
def show_gui(city, weather, outfit):
    root = tk.Tk()
    root.title("🌦️ Live Weather Notifier with AI")
    root.geometry("450x350")

    tk.Label(root, text=f"City: {city}", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(root, text=f"Temperature: {weather['temperature']} °C").pack()
    tk.Label(root, text=f"Humidity: {weather['humidity']}%").pack()
    tk.Label(root, text=f"Wind Speed: {weather['wind']} m/s").pack()
    tk.Label(root, text=f"Condition: {weather['description'].capitalize()}").pack(pady=10)
    tk.Label(root, text="👕 Outfit Suggestion:", font=("Helvetica", 12, "bold")).pack()
    tk.Message(root, text=outfit, width=400, fg="blue").pack(pady=10)

    root.mainloop()

# -----------------------------
# Main execution
# -----------------------------
def main():
    city = get_city()
    if not city:
        messagebox.showerror("Error", "City not recognized.")
        return

    weather = get_weather(city)
    if not weather:
        messagebox.showerror("Error", "Could not fetch weather data.")
        return

    outfit = suggest_outfit(weather["temperature"], weather["humidity"], weather["description"])
    show_gui(city, weather, outfit)

# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main()


