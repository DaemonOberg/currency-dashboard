
# SEK Currency Dashboard

A web application built with Python and Flask that allows users to compare the Swedish krona (SEK) against five currencies: EUR, USD, GBP, NOK, and DKK.

The dashboard provides current exchange rates, historical trends, currency conversions, and interactive charts.

## Features

- Compare SEK against one or more supported currencies.
- Convert a selected SEK amount into other currencies.
- Explore historical exchange rates over the past 12 months.
- Switch between interactive Plotly line and bar charts.
- Group historical exchange rates by day, week, month, or quarter.
- View percentage changes in exchange rates.
- Handle API errors and invalid user input.

## Technologies Used

- **Python** – Backend programming language
- **Flask** – Web application framework
- **Requests** – Fetching exchange rates from the API
- **Pandas** – Processing, grouping, and analyzing exchange rate data
- **Plotly** – Interactive data visualization
- **Jinja2** – HTML templates
- **HTML, CSS, JavaScript** – Frontend interface
- **Pytest** – Automated testing
- **Ruff** – Python linting and formatting

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DaemonOberg/currency-dashboard.git
cd currency-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Running the Application

Start the Flask development server:

```bash
python -m flask --app app run
```

Open your browser and visit:

http://127.0.0.1:5000

## How to Use

1. Enter an amount in SEK.
2. Select one or more currencies.
3. Click **Compare Currencies**.
4. View the historical exchange rate chart and currency conversion table.
5. Use **Switch Chart** to view percentage changes.
6. Select Day, Week, Month, or Quarter to change the historical grouping.

The Info page also provides instructions for answering three currency analysis questions.

## Running Tests

Run all automated tests:

```bash
python -m pytest -v
```

The tests cover API requests, calculation functions, Flask routes, and Plotly chart generation.

External API calls are mocked so the tests can run without an internet connection.

## Code Quality

Check Python code using Ruff:

```bash
ruff check .
```

Check formatting:

```bash
ruff format --check .
```

## Project Structure

```text
currency-dashboard/
├── static/
│   ├── css/
│   │   └── style.css
│   └── javascript/
│       └── results.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── info.html
│   └── results.html
├── tests/
│   ├── test_api.py
│   ├── test_app.py
│   ├── test_calculations.py
│   └── test_charts.py
├── api.py
├── app.py
├── calculations.py
├── charts.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Data Source

Exchange rate data is provided by the [Frankfurter API](https://frankfurter.dev/).

The application uses SEK as the base currency and retrieves current and historical exchange rates.

Frankfurter's software is licensed under the MIT License. Exchange rate data may be subject to the original data providers' terms of use.

For additional information, see the [Frankfurter License & Terms](https://frankfurter.dev/license/).

## Project Purpose

This project was developed as a group assignment to demonstrate:

- Building a web application using Flask.
- Integrating an external REST API.
- Processing data using Pandas.
- Creating interactive visualizations using Plotly.
- Writing automated tests with Pytest.
- Maintaining code quality with Ruff.
- Collaborating using Git and GitHub.
