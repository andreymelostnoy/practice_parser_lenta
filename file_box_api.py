import requests


file = "string"
detail = "string"

headers = {
    "Authorization": "Token token",
    "Accept": ""
}

dir = requests.get(dir, headers=headers)
print(dir.json())
