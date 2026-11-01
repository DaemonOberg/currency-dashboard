import plotly.express as px
import plotly.graph_objects as go


def create_charts(data, dates_by_currency, table_data, amount):
    """Create Plotly line and bar charts and return their HTML."""
    rates = data

    # Extract currencies and percentage changes for the bar chart
    currencies = [row["currency"] for row in table_data]
    changes = []
    for row in table_data:
        changes.append(row["change_12m"])

    # Create historical exchange rate line chart
    fig = go.Figure()

    # Add a separate line for each selected currency
    for currency, currency_rates in rates.items():
        fig.add_trace(
            go.Scatter(
                x=dates_by_currency[currency],
                y=[rate * amount for rate in currency_rates],
                mode="lines",
                name=f"{amount} SEK to {currency}",
            ),
        )

    # Set chart title, size and dark theme
    fig.update_layout(
        title=f"Historical Value of {amount:g} SEK in Selected Currencies",
        autosize=True,
        height=450,
        template="plotly_dark",
        paper_bgcolor="#0b1012",
        plot_bgcolor="#0b1012",
    )

    # Label the axes and use a logarithmic scale for exchange values
    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="Amount in Selected Currencies",
        yaxis_type="log",
    )

    # Display dates in year-month-day format
    fig.update_xaxes(tickformat="%Y-%m-%d")

    # Convert the line chart into responsive HTML for Jinja2
    line_html = fig.to_html(
        full_html=False,
        default_width="100%",
        config={"responsive": True},
    )

    # Create percentage change bar chart
    bar_fig = px.bar(
        x=currencies,
        y=changes,
        title="Currency Percentage Change",
        text=changes,
    )

    # Apply the same responsive layout and dark theme
    bar_fig.update_layout(
        autosize=True,
        height=450,
        template="plotly_dark",
        paper_bgcolor="#0b1012",
        plot_bgcolor="#0b1012",
    )

    # Label the bar chart axes
    bar_fig.update_layout(
        xaxis_title="Currencies",
        yaxis_title="Percentage Change (%)",
    )

    # Display percentage values above the bars
    bar_fig.update_traces(
        textposition="outside",
        texttemplate="%{text}%",
    )

    # Convert the bar chart into responsive HTML for Jinja2
    bar_html = bar_fig.to_html(
        full_html=False,
        default_width="100%",
        config={"responsive": True},
    )

    # Return both charts to the Flask results route
    return line_html, bar_html
