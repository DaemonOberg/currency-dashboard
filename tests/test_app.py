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
    response = client.get("/results?currencies=EUR&currencies=USD")
    # Kollar att sidan laddas utan fel
    assert response.status_code == 200
    # Kollar att grafen finns med på sidan
    assert b"EUR to SEK Exchange Rate" in response.data
