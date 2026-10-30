from flask import Flask, jsonify, render_template, request

from api import get_history, get_latest
from calculations import build_df, get_table_data, group_by_time
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
    df = build_df(history, selected_currencies)
    table_data = get_table_data(df)
    selected_period = request.args.get("period", "Day")
    grouped_df = group_by_time(df, selected_period)
    grouped_history = {}
    grouped_dates_by_currency = {}
    for _, row in grouped_df.iterrows():
        currency = row["currency"]

        if currency not in grouped_history:
            grouped_history[currency] = []
            grouped_dates_by_currency[currency] = []

        grouped_history[currency].append(row["sek"])
        grouped_dates_by_currency[currency].append(row["date"])

    line_html, bar_html = create_charts(
        grouped_history, grouped_dates_by_currency, table_data
    )
    return render_template(
        "results.html",
        selected_currencies=selected_currencies,
        line_html=line_html,
        bar_html=bar_html,
        rates=rates,
        selected_period=selected_period,
    )


@app.route("/api/chart")
def chart_data():
    selected_period = request.args.get("period")
    return jsonify(period=selected_period)
