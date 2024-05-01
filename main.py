import json
import os
from openai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv("OPEN_AI_KEY"))

def get_current_weather(location, unit="fahrenheit"):
    """ Get the current weather in the current location """
    if 'tokyo' in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    if 'paris' in location.lower():
        return json.dumps({"location": "Paris", "temperature": "10", "unit": unit})
    if 'san francisco' in location.lower():
        return json.dumps({"location": "san francisco", "temperature": "10", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def run_conversations():
    messages = [{"role": "user", "content": "What's the weather like in Tokyo, Paris and San Francisco?"}]
    tools = [
        {
            "type": "function",
            "function" : {
                "name": "get_current_weather",
                "description": "get the current weather at a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state for example San Franciso, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celcius", "fahrenheit"]
                        }
                    },
                    "required": ["location"],
                }
            }
        }
    ]
    
    response = client.chat.completions.create(
        model= "gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print(f"Tool Calls {tool_calls}", )
    
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
        }
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            funtion_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = funtion_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
        
run_conversations()