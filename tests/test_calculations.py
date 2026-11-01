from calculations import (
    build_df,
    calc_percent,
    get_table_data,
    group_by_time,
)

# Sample exchange rate data used in the tests
test_data = [
    {"date": "2025-03-10", "base": "SEK", "quote": "EUR", "rate": 0.20},
    {"date": "2025-03-11", "base": "SEK", "quote": "EUR", "rate": 0.10},
    {"date": "2025-03-10", "base": "SEK", "quote": "USD", "rate": 0.08},
    {"date": "2025-03-11", "base": "SEK", "quote": "USD", "rate": 0.10},
]


# Test converting API data into a DataFrame for a selected currency
def test_build_df():
    df = build_df(test_data, ["EUR"])

    assert not df.empty
    assert len(df) == 2
    assert df["sek"].iloc[0] == 0.20
    assert df["sek"].iloc[1] == 0.10


# Test that empty API data produces an empty DataFrame
def test_build_df_empty():
    df = build_df([], ["EUR"])
    assert df.empty


# Test grouping exchange rates by month and calculating the average
def test_group_by_time():
    df = build_df(test_data, ["EUR"])
    grouped = group_by_time(df, "Month")

    # The average of 0.20 and 0.10 is 0.15
    assert len(grouped) == 1
    assert grouped["date"].iloc[0] == "2025-03"
    assert grouped["sek"].iloc[0] == 0.15


# Test calculating percentage changes between consecutive exchange rates
def test_calc_percent():
    df = build_df(test_data, ["EUR"])
    res = calc_percent(df)

    # A decrease from 0.20 to 0.10 equals -50%
    assert "pct_change" in res.columns
    assert res["pct_change"].iloc[0] == 0.0
    assert res["pct_change"].iloc[1] == -50.0


# Test calculating currency statistics for the results table
def test_get_table_data():
    df = build_df(test_data, ["USD"])
    table = get_table_data(df)

    # An increase from 0.08 to 0.10 equals 25%
    assert len(table) == 1
    assert table[0]["currency"] == "USD"
    assert table[0]["latest_sek"] == 0.10
    assert table[0]["max_sek"] == 0.10
    assert table[0]["min_sek"] == 0.08
    assert table[0]["change_12m"] == 25.0


# Test grouping exchange rates by week and quarter
def test_group_by_time_periods():
    df = build_df(test_data, ["EUR"])
    week = group_by_time(df, "Week")
    quarter = group_by_time(df, "Quarter")

    assert len(week) == 1
    assert quarter["date"].iloc[0] == "2025-Q1"


# Test that calculation functions handle empty DataFrames
def test_empty_dataframes():
    empty_df = build_df([], ["EUR"])

    assert group_by_time(empty_df).empty
    assert calc_percent(empty_df).empty
    assert get_table_data(empty_df) == []
