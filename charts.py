import plotly.express as px
import plotly.graph_objects as go


def create_charts(data, dates_by_currency, table_data, amount):
    rates = data
    currencies = [row["currency"] for row in table_data]
    changes = []
    for row in table_data:
        changes.append(row["change_12m"])

    fig = go.Figure()

    for currency, currency_rates in rates.items():
        fig.add_trace(
            go.Scatter(
                x=dates_by_currency[currency],
                y=[rate * amount for rate in currency_rates],
                mode="lines",
                name=f"{amount} SEK to {currency}",
            ),
        )

    fig.update_layout(
        title=f"Historical Value of {amount:g} SEK in Selected Currencies",
        height=450,
        template="plotly_dark",
        paper_bgcolor="#0b1012",
        plot_bgcolor="#0b1012",
    )
    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="Amount in Selected Currencies",
        yaxis_type="log",
    )
    fig.update_xaxes(tickformat="%Y-%m-%d")
    line_html = fig.to_html()

    bar_fig = px.bar(
        x=currencies, 
        y=changes, 
        title="Currency Percentage Change", 
        text=changes
    )
    bar_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1012",
    plot_bgcolor="#0b1012"
    )
    bar_fig.update_layout(
        xaxis_title="Currencies", 
        yaxis_title="Percentage Change (%)"
    )
    bar_fig.update_traces(
        textposition="outside",
        texttemplate="%{text}%"
    )
    bar_html = bar_fig.to_html()

    return line_html, bar_html
