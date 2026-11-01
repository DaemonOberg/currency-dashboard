from calculations import (
    build_df,
    calc_percent,
    convert_to_sek,
    get_answers,
    get_table_data,
    group_by_time,
)

test_data = [
    {"date": "2025-03-10", "base": "SEK", "quote": "EUR", "rate": 0.20},
    {"date": "2025-03-11", "base": "SEK", "quote": "EUR", "rate": 0.10},
    {"date": "2025-03-10", "base": "SEK", "quote": "USD", "rate": 0.08},
    {"date": "2025-03-11", "base": "SEK", "quote": "USD", "rate": 0.10},
]


def test_build_df():
    df = build_df(test_data, ["EUR"])

    assert not df.empty
    assert len(df) == 2
    assert df["sek"].iloc[0] == 0.20
    assert df["sek"].iloc[1] == 0.10


def test_build_df_empty():
    df = build_df([], ["EUR"])
    assert df.empty


def test_group_by_time():
    df = build_df(test_data, ["EUR"])
    grouped = group_by_time(df, "Month")

    # medelvärdet av 0.20 och 0.10 i mars blir 0.15
    assert len(grouped) == 1
    assert grouped["date"].iloc[0] == "2025-03"
    assert grouped["sek"].iloc[0] == 0.15


def test_calc_percent():
    df = build_df(test_data, ["EUR"])
    res = calc_percent(df)

    # från 0.20 ner till 0.10 är en minskning på 50 procent
    assert "pct_change" in res.columns
    assert res["pct_change"].iloc[0] == 0.0
    assert res["pct_change"].iloc[1] == -50.0


def test_get_table_data():
    df = build_df(test_data, ["USD"])
    table = get_table_data(df)

    # från 0.08 upp till 0.10 är en ökning på 25 procent
    assert len(table) == 1
    assert table[0]["currency"] == "USD"
    assert table[0]["latest_sek"] == 0.10
    assert table[0]["max_sek"] == 0.10
    assert table[0]["min_sek"] == 0.08
    assert table[0]["change_12m"] == 25.0


def test_get_answers():
    df = build_df(test_data, ["EUR", "USD"])
    answers = get_answers(df)

    assert answers["eur_change"] == -50.0
    assert answers["strongest"] == "USD"
    assert answers["weakest"] == "EUR"
    assert answers["highest"] == "EUR"


def test_convert_to_sek():
    latest = [{"date": "2025-03-11", "base": "SEK", "quote": "USD", "rate": 0.08}]
    res = convert_to_sek(100, "USD", latest)

    # 1 / 0.08 = 12.5 kr per dollar -> 100 dollar = 1250 kr
    assert res["rate"] == 12.5
    assert res["sek_amount"] == 1250.0


# Testar vecka och kvartal i group_by_time
def test_group_by_time_periods():
    df = build_df(test_data, ["EUR"])
    week = group_by_time(df, "Week")
    quarter = group_by_time(df, "Quarter")

    assert len(week) == 1
    assert quarter["date"].iloc[0] == "2025-Q1"


# Testar att funktionerna hanterar en tom dataframe utan att krascha
def test_empty_dataframes():
    empty_df = build_df([], ["EUR"])

    assert group_by_time(empty_df).empty
    assert calc_percent(empty_df).empty
    assert get_table_data(empty_df) == []
    assert get_answers(empty_df) == {}


# Testar convert_to_sek när data eller valuta saknas
def test_convert_to_sek_missing():
    latest = [{"date": "2025-03-11", "base": "SEK", "quote": "USD", "rate": 0.08}]

    assert convert_to_sek(100, "USD", []) is None
    assert convert_to_sek(100, "GBP", latest) is None
