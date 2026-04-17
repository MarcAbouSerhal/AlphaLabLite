import requests

# POST /execute
response = requests.post(
    "http://127.0.0.1:8000/execute",
    json={"script": "btc = Fetch{OneMinuteBitcoinPrices}{}\neth = Fetch{OneMinuteEthereum}{}"}
)
result = response.json()
print(result)

# GET /view/{id}
id = result["result"]
response = requests.get(
    f"http://127.0.0.1:8000/view/{id}",
    params={"items": ["btc", "eth"]}
)
print(response.json())