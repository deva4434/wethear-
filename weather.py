# # import required modules
# import requests, json
# Enter your API key here

import pyttsx3
import speech_recognition as sr
import requests
import json

def speak(text):
    engine = pyttsx3.init()
    ID = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    voices = engine.getProperty('voices')
    engine.setProperty('voice' , ID)
    print("")
    print(f"==> Jarvis AI : {text}")
    print("")
    engine.say(text=text)
    engine.runAndWait()

def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        return query.lower()
    except:
        return ""

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            temperature = data['main']['temp']
        except KeyError:
            print("Temperature data not found.")
            temperature = None

        try:
            rain_chance = data['rain']['1h'] if 'rain' in data else 0
        except KeyError:
            print("Rain data not found.")
            rain_chance = 0

        return temperature, rain_chance
    else:
        print(f"Error: {data['message']}")
        return None

# Replace 'your_api_key' with your actual OpenWeatherMap API key
api_key = 'your_api_key'
while True:
    print("Enter city")
    city = speechrecognition()
    result = get_weather(api_key, city)

    if result:
        temperature, rain_chance = result
        speak(f'Temperature in {city}: {temperature}°C')
        # s(f'Rain Chance: {rain_chance} mm/hour')
