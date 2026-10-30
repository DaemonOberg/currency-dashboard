from flask import Flask, jsonify, render_template, request

from api import get_history, get_latest
from charts import create_charts

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    selected_currencies = request.args.getlist("currencies")
    rates = get_latest(selected_currencies)
    history = get_history(selected_currencies)
    dates = []
    rates_history = {}

    for record in history:
        currency = record["quote"]

        if currency not in rates_history:
            rates_history[currency] = []

        rates_history[currency].append(1 / record["rate"])

        if record["date"] not in dates:
            dates.append(record["date"])

    selected_period = request.args.getlist("period")
    print("API-svar:", selected_period, rates)
    line_html, bar_html = create_charts(rates_history, dates)
    return render_template(
        "results.html",
        selected_currencies=selected_currencies,
        line_html=line_html,
        bar_html=bar_html,
        rates=rates,
    )


@app.route("/api/chart")
def chart_data():
    selected_period = request.args.get("period")
    return jsonify(period=selected_period)
