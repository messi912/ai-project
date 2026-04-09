import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

system_prompt = """You are a helpful weather assistant. The user will ask you 
questions about weather, forecasts, and climate. Answer conversationally and 
helpfully. If the user asks about current weather for a specific city, let them 
know you can fetch real live data for them."""

print("Weather Assistant ready! Type 'quit' to exit.\n")

while True:
    user_input = input("> ")
    
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
    
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    print(f"\nAssistant: {assistant_message}\n")