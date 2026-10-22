from flask import Flask, render_template, request

from charts import create_charts

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    selected_currencies = request.args.getlist("currencies")
    line_html, bar_html = create_charts()
    return render_template(
        "results.html",
        selected_currencies=selected_currencies,
        line_html=line_html,
        bar_html=bar_html,
    )
