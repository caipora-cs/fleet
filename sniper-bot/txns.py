import json
import requests


response = requests.get(
    "https://api.dexscreener.com/latest/dex/pairs/base/0x2114cf47f9932250291011d400715aea6adb61ae",
    timeout=10,
)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))

    with open("screener.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
else:
    print("Failed to retrieve data from the API")


print(data)
