from flask import Flask, render_template, request, jsonify
from plot import Plot
import datetime


def getData(code__):
    plot = Plot(title=code__, code__=code__,
                start=datetime.datetime(2021, 7, 1),
                end=datetime.datetime.now())
    plot.plotSegment()
    plot.plotRect()
    return plot.embed()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", plot=None)


@app.route('/getPlot', methods=["POST"])
def getPlot():
    if request.method == "POST":
        # Getting data from form
        code__ = request.form["companyCode"]
        try:
            return jsonify(error=None, data=getData(code__))
        except:
            return jsonify(error="Data not found", data=None)


if __name__ == '__main__':
    app.run(debug=True)
