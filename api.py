from datetime import date, timedelta

import requests

URL = "https://api.frankfurter.dev/v2/rates"
VALUTOR = ["EUR", "USD", "GBP", "NOK", "JPY"]


def get_latest(currencies=None):
    # om inget skickas med kör vi standardlistan
    if currencies is None:
        currencies = VALUTOR

    # tar bort sek från listan eftersom sek är basvaluta
    quotes_list = [c for c in currencies if c != "SEK"]

    params = {"base": "SEK", "quotes": ",".join(quotes_list)}

    try:
        # gör anrop med timeout så appen inte hänger sig
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as err:
        print(f"kunde inte hämta data: {err}")
        return None


def get_history(currencies=None, start=None, end=None):
    if currencies is None:
        currencies = VALUTOR

    # sätter datum ett år bakåt om man inte valt något annat
    if end is None:
        end = str(date.today())
    if start is None:
        start = str(date.today() - timedelta(days=365))

    quotes_list = [c for c in currencies if c != "SEK"]

    params = {
        "from": start,
        "to": end,
        "base": "SEK",
        "quotes": ",".join(quotes_list),
    }

    try:
        res = requests.get(URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as err:
        print(f"kunde inte hämta historik: {err}")
        return None
