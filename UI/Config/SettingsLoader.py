import json

with open('PredefinedActionMap.json', encoding='UTF-8') as f:
    data = json.load(f)

for key, action in data.items():
    print(key)
    print(action)