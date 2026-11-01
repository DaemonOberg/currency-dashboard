from charts import create_charts


# Test that both Plotly charts are generated correctly
def test_create_charts():
    # Generate charts using sample exchange rate data
    line_html, bar_html = create_charts(
        data={"EUR": [0.09, 0.10]},
        dates_by_currency={"EUR": ["2026-01-01", "2026-01-02"]},
        table_data=[{"currency": "EUR", "change_12m": 11.11}],
        amount=100,
    )

    # Check that both charts return HTML strings
    assert isinstance(line_html, str)
    assert isinstance(bar_html, str)

    # Check that both charts contain the expected titles
    assert "Historical Value of 100 SEK" in line_html
    assert "Currency Percentage Change" in bar_html
