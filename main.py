# Importing Modules
from flask import Flask, render_template, request, jsonify
from data import StockData
import datetime
import json


# Function to format increased & decreased data in format required by canvas js
def formatData(data__):
    list__ = []
    for item in data__:
        date__ = [int(item) for item in str(item).split(" ")[0].split("-")]
        list__.append({"x": [date__[0], date__[1], date__[2]],
                       "y": [
                           data__[item]["Open"],
                           data__[item]["High"],
                           data__[item]["Low"],
                           data__[item]["Close"]
                       ]})
    return list__


# Function to get data from yahoo
def getData(code__, start__, end__):
    data__ = StockData(code__,
                       datetime.datetime.strptime(start__, '%Y-%m-%d').date(),
                       datetime.datetime.strptime(end__, '%Y-%m-%d').date())
    return [formatData(data__.increase_days()), formatData(data__.decrease_days())]


# Collecting company names
with open("data.json") as f:
    company_name = sorted(json.load(f), key=lambda i: i['name'])

# Creating app
app = Flask(__name__)


@app.route('/')
def home():
    # Main route
    name_list__ = []
    for item in company_name:
        name_list__.append(item["name"] + " / " + item["symbol"])
    return render_template("index.html", names=name_list__)


@app.route('/getPlot', methods=["POST"])
def getPlot():
    # Getting data for plotting in html
    if request.method == "POST":
        # Getting data from form
        code__ = request.args.get("code").upper()
        start__ = request.args.get("start")
        end__ = request.args.get("end")

        title__ = ""

        # Getting company name by code
        for item in company_name:
            if item["symbol"] == code__:
                title__ = item["name"]
                break

        try:
            # If data is found with no error
            return jsonify(error=None, data=getData(code__, start__, end__), title=title__)
        except:
            # If some error occurred due to user inputs
            return jsonify(error="Data not found", data=None)


if __name__ == '__main__':
    app.run()
