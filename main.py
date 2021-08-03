from flask import Flask, render_template
from plot import Plot
import datetime

plot = Plot(title="Google Chart",
            start=datetime.datetime(2021, 7, 1),
            end=datetime.datetime.now())
plot.plotSegment()
plot.plotRect()
script, html, cdn_js = plot.embed()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html",
                           script=script,
                           html=html,
                           cdn_js=cdn_js)


if __name__ == '__main__':
    app.run(debug=True)
