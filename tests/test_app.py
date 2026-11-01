from unittest.mock import patch

import pytest

from app import app


# Create a Flask test client for testing routes
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test that the home page loads successfully
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


# Test the results page using mocked exchange rate data
@patch("app.get_latest")
@patch("app.get_history")
def test_results(mock_history, mock_latest, client):
    mock_latest.return_value = [
        {"date": "2026-01-02", "base": "SEK", "quote": "EUR", "rate": 0.09},
        {"date": "2026-01-02", "base": "SEK", "quote": "USD", "rate": 0.10},
    ]

    mock_history.return_value = [
        {"date": "2026-01-01", "base": "SEK", "quote": "EUR", "rate": 0.08},
        {"date": "2026-01-02", "base": "SEK", "quote": "EUR", "rate": 0.09},
        {"date": "2026-01-01", "base": "SEK", "quote": "USD", "rate": 0.09},
        {"date": "2026-01-02", "base": "SEK", "quote": "USD", "rate": 0.10},
    ]

    response = client.get("/results?amount=100&currencies=EUR&currencies=USD")

    assert response.status_code == 200
    assert b"Historical Value of 100 SEK" in response.data


# Test the results page when no currency is selected
def test_results_missing_currencies(client):
    response = client.get("/results?amount=100")

    assert response.status_code == 200
    assert b"Please select a currency" in response.data


# Test the results page when no amount is provided
def test_results_missing_amount(client):
    response = client.get("/results?currencies=EUR")

    assert response.status_code == 200
    assert b"Please enter an amount" in response.data


# Test the results page when the amount is invalid
def test_results_invalid_amount(client):
    response = client.get("/results?amount=abc&currencies=EUR")

    assert response.status_code == 200
    assert b"Please enter a valid number" in response.data


# Test that the information page loads successfully
def test_info(client):
    response = client.get("/info")

    assert response.status_code == 200


# Test the chart API endpoint using mocked historical data
@patch("app.get_history")
def test_api_chart(mock_history, client):
    mock_history.return_value = [
        {"date": "2026-01-01", "base": "SEK", "quote": "EUR", "rate": 0.08},
        {"date": "2026-01-02", "base": "SEK", "quote": "EUR", "rate": 0.09},
    ]

    response = client.get("/api/chart?period=Month&currencies=EUR")

    assert response.status_code == 200


# Test the results page when the API fails
@patch("app.get_latest")
@patch("app.get_history")
def test_results_api_error(mock_history, mock_latest, client):
    mock_latest.return_value = None
    mock_history.return_value = None

    response = client.get("/results?amount=100&currencies=EUR")

    assert response.status_code == 200
