import json
import pandas as pd

if __name__ == '__main__':
    # Getting data from csv file
    csv_file = pd.read_csv("data.csv")
    csv_file.fillna("", inplace=True)
    dict__ = csv_file.T.to_dict()
    list__ = []

    for item in dict__:
        list__.append(dict__[item])

    list__ = sorted(list__, key=lambda i: str(i['COMPANY']))

    # Storing complete type of data in one file
    data = {}
    with open("exchange.json") as f:
        temp__ = json.load(f)
        for item in temp__:
            data[item] = {"exchanges": []}
            for ex in temp__[item]:
                data[item]["exchanges"].append(ex)
                data[item][ex] = []
            data[item]["exchanges"].append("Other")
            data[item]["Other"] = []

    for stockData in list__:
        cont = stockData["COUNTRY"]
        exc = stockData["EXCHANGE"]
        if cont == "New Zeland":
            cont = "New Zealand"
        if exc == "":
            exc = "Other"
        data[cont][exc].append(stockData["COMPANY"] + " / " + stockData["SYMBOL"])

    # Removing those countries or exchanges which does not have a single stock
    fin_data = {}
    for country in data:
        fin_data[country] = {"exchanges": []}
        for exchange in data[country]["exchanges"]:
            if len(data[country][exchange]) != 0:
                fin_data[country]["exchanges"].append(exchange)
                fin_data[country][exchange] = data[country][exchange]
        if len(fin_data[country]["exchanges"]) == 0:
            fin_data.pop(country)

    # Getting company names to show on plot
    company_names = {}
    for country in fin_data:
        for exchange in fin_data[country]["exchanges"]:
            for stock in fin_data[country][exchange]:
                value, key = str(stock).split(" / ")
                company_names[key] = value
    with open("company.json", "w") as f:
        json.dump(company_names, f)

    # Getting final json file
    with open("data.json", "w") as f:
        json.dump(fin_data, f)
