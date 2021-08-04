from flask import Flask, render_template, request, jsonify
from plot import Plot
import datetime


def getData(code__, start__, end__):
    plot = Plot(title=code__, code__=code__,
                start=datetime.datetime.strptime(start__, '%Y-%m-%d').date(),
                end=datetime.datetime.strptime(end__, '%Y-%m-%d').date())
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
        start__ = request.form["startDate"]
        end__ = request.form["endDate"]
        try:
            return jsonify(error=None, data=getData(code__, start__, end__))
        except:
            return jsonify(error="Data not found", data=None)


if __name__ == '__main__':
    app.run(debug=True)
