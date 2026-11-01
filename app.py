import math

from flask import Flask, jsonify, render_template, request

from api import get_history, get_latest
from calculations import build_df, get_table_data, group_by_time
from charts import create_charts

# Create the Flask application
app = Flask(__name__)


@app.route("/")
def index():
    """Display the home page with the currency selection form."""
    return render_template("index.html")


@app.route("/results")
def results():
    """Validate user input and display currency charts and conversions."""

    # Get the currencies selected by the user
    selected_currencies = request.args.getlist("currencies")
    if not selected_currencies:
        return render_template("index.html", error="Please select a currency")

    # Get and validate the entered SEK amount
    amount = request.args.get("amount")
    if not amount:
        return render_template("index.html", error="Please enter an amount")

    try:
        amount = float(amount)
    except ValueError:
        return render_template("index.html", error="Please enter a valid number")

    # Reject negative, zero and non-finite amounts
    if not math.isfinite(amount) or amount <= 0:
        return render_template(
            "index.html",
            error="Please enter a positive, finite amount",
        )

    # Fetch current and historical exchange rates from the API
    rates = get_latest(selected_currencies)
    history = get_history(selected_currencies)

    # Display an error message if the API request fails
    if rates is None or history is None:
        return render_template(
            "index.html",
            error="Could not retrieve exchange rates. Please try again later.",
        )

    # Convert API data into a DataFrame and calculate currency statistics
    df = build_df(history, selected_currencies)
    table_data = get_table_data(df)

    # Group historical rates by the selected time period
    selected_period = request.args.get("period", "Day")
    grouped_df = group_by_time(df, selected_period)

    # Prepare exchange rates and dates for each currency chart
    grouped_history = {}
    grouped_dates_by_currency = {}

    for _, row in grouped_df.iterrows():
        currency = row["currency"]

        if currency not in grouped_history:
            grouped_history[currency] = []
            grouped_dates_by_currency[currency] = []

        grouped_history[currency].append(row["sek"])
        grouped_dates_by_currency[currency].append(row["date"])

    # Generate the Plotly line and bar charts
    line_html, bar_html = create_charts(
        grouped_history, grouped_dates_by_currency, table_data, amount
    )

    # Render the results page with charts and conversion data
    return render_template(
        "results.html",
        selected_currencies=selected_currencies,
        line_html=line_html,
        bar_html=bar_html,
        rates=rates,
        selected_period=selected_period,
        table_data=table_data,
        amount=amount,
    )


@app.route("/api/chart")
def chart_data():
    """Return grouped historical exchange rates as JSON for JavaScript."""

    # Read the selected period and currencies from the URL
    selected_period = request.args.get("period")
    selected_currencies = request.args.getlist("currencies")

    # Fetch historical exchange rates
    history = get_history(selected_currencies)

    if history is None:
        return jsonify(error="Could not retrieve historical exchange rates."), 503

    # Group exchange rates by the requested period
    df = build_df(history, selected_currencies)
    grouped_df = group_by_time(df, selected_period)

    # Convert the DataFrame into JSON-compatible records
    chart_records = grouped_df.to_dict(orient="records")

    return jsonify(period=selected_period, records=chart_records)


@app.route("/info")
def info():
    """Display project information and the currency analysis guide."""
    return render_template("info.html")
