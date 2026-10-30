import plotly.express as px


def create_charts(data, dates):
    rates = data
    currencies = ["EUR", "USD", "GBP"]
    changes = [1.2, -0.5, 0.8]

    fig = px.line(x=dates, y=rates, title="EUR to SEK Exchange Rate", markers=True)
    fig.update_layout(xaxis_title="Dates", yaxis_title="Exchange Rate (SEK)")
    fig.update_xaxes(tickformat="%Y-%m-%d")
    line_html = fig.to_html()

    bar_fig = px.bar(
        x=currencies, y=changes, title="Currency Percentage Change", text=changes
    )
    bar_fig.update_layout(xaxis_title="Currencies", yaxis_title="Percentage Change (%)")
    bar_fig.update_traces(textposition="outside", texttemplate="%{text}%")
    bar_html = bar_fig.to_html()

    return line_html, bar_html
