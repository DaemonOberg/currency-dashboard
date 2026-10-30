from flask import Flask, jsonify, render_template, request

from api import get_latest
from charts import create_charts

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    rates = get_latest()
    data = [15, 10.7, 10.6]
    dates = ["2026-10-20", "2026-10-21", "2026-10-22"]
    selected_currencies = request.args.getlist("currencies")
    selected_period = request.args.getlist("period")
    print(selected_period,rates)
    line_html, bar_html = create_charts(data, dates)
    return render_template(
        "results.html",
        selected_currencies=selected_currencies,
        line_html=line_html,
        bar_html=bar_html,
    )


@app.route("/api/chart")
def chart_data():
    selected_period = request.args.get("period")
    return jsonify(period=selected_period)
