import requests

#https://api.broken-url.com  https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true
def get_coordinates(city):
    try:
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
        data = response.json()

        if not data.get("results"):
            return None

        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"], result["country"]
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None

def get_weather(latitude, longitude):
    try:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
        data = response.json()
        return data["current_weather"]
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None
weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
}