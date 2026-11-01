from datetime import date, timedelta

import requests

# Frankfurter API endpoint and supported currencies
URL = "https://api.frankfurter.dev/v2/rates"
VALUTOR = ["EUR", "USD", "GBP", "NOK", "DKK"]


def get_latest(currencies=None):
    """Fetch the latest exchange rates with SEK as the base currency."""

    # Use the default currencies if none are provided
    if currencies is None:
        currencies = VALUTOR

    # Exclude SEK because it is the base currency
    quotes_list = [c for c in currencies if c != "SEK"]

    params = {"base": "SEK", "quotes": ",".join(quotes_list)}

    try:
        # Set a timeout to prevent the application from waiting indefinitely
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.RequestException as err:
        print(f"Could not retrieve exchange rates: {err}")
        return None


def get_history(currencies=None, start=None, end=None):
    """Fetch historical exchange rates for the selected currencies."""

    # Use the default currencies if none are provided
    if currencies is None:
        currencies = VALUTOR

    # Use the past 365 days if no date range is provided
    if end is None:
        end = str(date.today())
    if start is None:
        start = str(date.today() - timedelta(days=365))

    # Exclude SEK because it is the base currency
    quotes_list = [c for c in currencies if c != "SEK"]

    params = {
        "from": start,
        "to": end,
        "base": "SEK",
        "quotes": ",".join(quotes_list),
    }

    try:
        # Fetch historical data with a five-second timeout
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.RequestException as err:
        print(f"Could not retrieve historical exchange rates: {err}")
        return None
