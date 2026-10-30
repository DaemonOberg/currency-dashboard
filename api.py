from datetime import date, timedelta

import requests

URL = "https://api.frankfurter.dev/v2/rates"
VALUTOR = ["EUR", "USD", "GBP", "NOK", "JPY"]


def get_latest(currencies=None):
    if currencies is None:
        currencies = VALUTOR

    quotes = []
    for c in currencies:
        if c != "EUR":
            quotes.append(c)

    # SEK behövs alltid för att räkna om från EUR
    if "SEK" not in quotes:
        quotes.append("SEK")

    params = {"quotes": ",".join(quotes)}

    try:
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as err:
        print(f"Fel vid API-anrop: {err}")
        return None


def get_history(currencies=None, start=None, end=None):
    if currencies is None:
        currencies = VALUTOR

    # om inga datum skickas med tar vi senaste året
    if end is None:
        end = str(date.today())
    if start is None:
        start = str(date.today() - timedelta(days=365))

    quotes = []
    for c in currencies:
        if c != "EUR":
            quotes.append(c)

    if "SEK" not in quotes:
        quotes.append("SEK")

    params = {
        "from": start,
        "to": end,
        "quotes": ",".join(quotes),
    }

    try:
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as err:
        print(f"Fel vid hämtning av historik: {err}")
        return None
