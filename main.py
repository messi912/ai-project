import anthropic
import os
from dotenv import load_dotenv
from weather import get_coordinates, get_weather, weather_codes

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

system_prompt = """You are a helpful weather assistant. You have access to real 
live weather data. When the user asks about the weather in a specific city, 
extract the city name from their message and include it in your response in 
this exact format on its own line: FETCH_WEATHER: <city name>

For example if someone asks "what's the weather in Paris?", include this line:
FETCH_WEATHER: Paris

For all other questions just respond conversationally. Do not make up weather 
data - only report data that is provided to you."""

def fetch_weather_for_city(city):
    coordinates = get_coordinates(city)
    if coordinates is None:
        return f"Sorry, I couldn't find the city '{city}'."
    
    latitude, longitude, name, country = coordinates
    weather = get_weather(latitude, longitude)
    
    if weather is None:
        return f"Sorry, I couldn't fetch weather data for {city}."
    
    code = weather["weathercode"]
    description = weather_codes.get(code, "Unknown conditions")
    
    return f"Current weather in {name}, {country}: {description}, {weather['temperature']}°C, wind speed {weather['windspeed']} km/h."

print("Weather Assistant ready! Type 'quit' to exit.\n")

while True:
    user_input = input(">  ")
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    
    if "FETCH_WEATHER:" in assistant_message:
        lines = assistant_message.split("\n")
        city = None
        for line in lines:
            if line.startswith("FETCH_WEATHER:"):
                city = line.replace("FETCH_WEATHER:", "").strip()
                break
        
        if city:
            weather_data = fetch_weather_for_city(city)
            
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            conversation_history.append({
                "role": "user",
                "content": f"Here is the live weather data: {weather_data}. Now respond to the user with this information naturally."
            })
            
            final_response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1024,
                system=system_prompt,
                messages=conversation_history
            )
            
            assistant_message = final_response.content[0].text
    
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    print(f"\nAssistant: {assistant_message}\n")