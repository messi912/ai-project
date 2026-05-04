import anthropic
import os
from dotenv import load_dotenv
from weather import get_coordinates, get_weather, weather_codes

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = """You are a helpful weather assistant. You have access to real 
live weather data. When the user asks about the weather in a specific city, 
extract the city name from their message and include it in your response in 
this exact format on its own line: FETCH_WEATHER: <city name>

When the user asks what to wear, what to pack, or outfit suggestions for a city,
also use FETCH_WEATHER: <city name> to get the conditions first, then suggest
a specific outfit based on the temperature and conditions. Be specific and fun
with outfit suggestions — mention actual clothing items.

For example if someone asks "what should I wear in Tokyo today?", include:
FETCH_WEATHER: Tokyo

For all other questions just respond conversationally. Do not make up weather 
data - only report data that is provided to you."""


def fetch_weather_for_city(city):
    """Fetch live weather data for a given city and return a formatted string."""
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


def chat(conversation_history, user_input):
    """Send a message and return the assistant's response, fetching weather if needed."""
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=system_prompt,
            messages=conversation_history
        )
    except Exception as e:
        return f"Error communicating with AI: {e}"

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

            try:
                final_response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=1024,
                    system=system_prompt,
                    messages=conversation_history
                )
                assistant_message = final_response.content[0].text
            except Exception as e:
                return f"Error fetching AI response: {e}"

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message


def main():
    """Main entry point for the Weather Assistant CLI."""
    conversation_history = []
    print("Weather Assistant ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("> ")

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        response = chat(conversation_history, user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()