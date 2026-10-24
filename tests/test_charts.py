from charts import create_charts


# Testar att funktionen skapar graferna korrekt
def test_create_charts():
    # Kör funktionen och sparar båda graferna
    line_html, bar_html = create_charts()

    # Kollar att det som returneras är strängar (HTML)
    assert isinstance(line_html, str)
    assert isinstance(bar_html, str)

    # Kollar att rätt titlar finns med i HTML koden
    assert "EUR to SEK Exchange Rate" in line_html
    assert "Currency Percentage Change" in bar_html
