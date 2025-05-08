import re
import dateparser
import requests

url = "http://172.29.114.86:11434/api/chat"

# ------------- Farmer Message Parsing -------------
def parse_driver_message(message):
    payload = json={
        "model": "hingaTransit-AI",
        "messages": [{"role": "user", "content": message}],
        }
    response = requests.post(url, json=payload, stream=True)
    
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    return data
                except json.JSONDecodeError:
                    continue
    else:
        return {"error": "Failed to parse driver message"}
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to parse driver message"}

# ------------- Farmer Message Parsing -------------
def parse_farmer_message(message):
    response = requests.post(url, json={"text": message})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to parse farmer message"}