from unittest.mock import patch

import requests

from api import get_history, get_latest


# Test fetching the latest exchange rates using mocked API data
@patch("api.requests.get")
def test_get_latest(mock_get):
    data = [{"date": "2025-05-14", "base": "SEK", "quote": "EUR", "rate": 0.092}]
    mock_get.return_value.json.return_value = data

    res = get_latest(["EUR"])

    assert res == data
    assert res[0]["rate"] == 0.092


# Test error handling when fetching the latest exchange rates
@patch("api.requests.get")
def test_get_latest_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()

    res = get_latest(["EUR"])

    assert res is None


# Test fetching historical exchange rates using mocked API data
@patch("api.requests.get")
def test_get_history(mock_get):
    data = [{"date": "2025-03-10", "base": "SEK", "quote": "NOK", "rate": 1.05}]
    mock_get.return_value.json.return_value = data

    res = get_history(["NOK"], start="2025-03-01", end="2025-03-15")

    assert res == data
    assert res[0]["quote"] == "NOK"


# Test error handling when fetching historical exchange rates
@patch("api.requests.get")
def test_get_history_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()

    res = get_history(["NOK"])

    assert res is None
