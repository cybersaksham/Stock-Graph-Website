# Importing Modules
from flask import Flask, render_template, request, jsonify
from data import StockData
import datetime


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


# Creating app
app = Flask(__name__)


@app.route('/')
def home():
    # Main route
    return render_template("index.html", plot=None)


@app.route('/getPlot', methods=["POST"])
def getPlot():
    # Getting data for plotting in html
    if request.method == "POST":
        # Getting data from form
        code__ = request.form["companyCode"]
        start__ = request.form["startDate"]
        end__ = request.form["endDate"]

        try:
            # If data is found with no error
            return jsonify(error=None, data=getData(code__, start__, end__))
        except:
            # If some error occurred due to user inputs
            return jsonify(error="Data not found", data=None)


if __name__ == '__main__':
    app.run(debug=True)
