import requests
import json


def get_data():
    url = "https://api.iextrading.com/1.0/ref-data/symbols"

    result = requests.get(url).json()
    list__ = []
    for item in result:
        dict__ = {"symbol": item["symbol"], "name": item["name"]}
        if item["name"] != "":
            list__.append(dict__)
    with open("data.json", "w") as f:
        json.dump(list__, f)


get_data()
