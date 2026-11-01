from unittest.mock import patch

import pytest

from app import app


# Skapar testklient för att kunna anropa sidorna i testerna
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Testar att startsidan laddas som den ska
def test_index(client):
    response = client.get("/")
    # Kollar att statuskoden är 200
    assert response.status_code == 200


# Testar resultatsidan med valda valutor i URL:en
def test_results(client):
    response = client.get("/results?amount=100&currencies=EUR&currencies=USD")
    # Kollar att sidan laddas utan fel
    assert response.status_code == 200
    # Kollar att grafen finns med på sidan
    assert b"Historical Value of 100 SEK" in response.data


# Testar när man glömt att välja valuta
def test_results_missing_currencies(client):
    response = client.get("/results?amount=100")
    assert response.status_code == 200
    assert b"Please select a currency" in response.data


# Testar när man glömt att skriva in belopp
def test_results_missing_amount(client):
    response = client.get("/results?currencies=EUR")
    assert response.status_code == 200
    assert b"Please enter an amount" in response.data


# Testar när beloppet inte är ett giltigt tal (t.ex. text)
def test_results_invalid_amount(client):
    response = client.get("/results?amount=abc&currencies=EUR")
    assert response.status_code == 200
    assert b"Please enter a valid number" in response.data


# Testar att infosidan laddas utan fel
def test_info(client):
    response = client.get("/info")
    assert response.status_code == 200


# Testar diagram-endpointen som anropas via JavaScript
def test_api_chart(client):
    response = client.get("/api/chart?period=Month&currencies=EUR")
    assert response.status_code == 200


# Testar när API:et misslyckas och returnerar None
@patch("app.get_latest")
@patch("app.get_history")
def test_results_api_error(mock_history, mock_latest, client):
    mock_latest.return_value = None
    mock_history.return_value = None

    response = client.get("/results?amount=100&currencies=EUR")
    assert response.status_code == 200
