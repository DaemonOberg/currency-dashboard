import plotly.express as px


def create_charts():
    rates = [10.5, 10.7, 10.6]
    days = ["Day 1", "Day 2", "Day 3"]
    currencies = ["EUR", "USD", "GBP"]
    changes = [1.2, -0.5, 0.8]

    fig = px.line(x=days, y=rates, title="EUR to SEK Exchange Rate")
    fig.update_layout(xaxis_title="Days", yaxis_title="Exchange Rate (SEK)")
    line_html = fig.to_html()

    bar_fig = px.bar(x=currencies, y=changes, title="Currency Percentage Change")
    bar_fig.update_layout(xaxis_title="Currencies", yaxis_title="Percentage Change (%)")
    bar_html = bar_fig.to_html()

    return line_html, bar_html
