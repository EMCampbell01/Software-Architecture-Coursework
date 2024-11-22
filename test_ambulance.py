import requests
import json

# Define the URL for the new_callout endpoint
url = "http://localhost:4000/new_callout"

data = {
    "name": "Euan Campbell",
    "address": "Princes St, Edinburgh",
    "priority": 1,
    "hospital": "Edinburgh Royal Infirmary"
}

# Send the data as a POST request to the /new_callout API
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully sent the new callout!")
    print("Response:", response.json())
else:
    print("Failed to send new callout.")
    print("Status code:", response.status_code)
    print("Error:", response.text)
