import json
import requests


response = requests.get(
    "https://api.dexscreener.com/latest/dex/pairs/base/0x2114cf47f9932250291011d400715aea6adb61ae",
    timeout=10,
)
data = response.json()

print(data)
