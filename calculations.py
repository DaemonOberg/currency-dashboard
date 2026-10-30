import pandas as pd


def build_df(data, selected):
    if not data:
        return pd.DataFrame()

    rows = []
    for row in data:
        d = row["date"]
        curr = row["quote"]
        rate = row["rate"]

        if curr in selected:
            # räknar ut vad 1 enhet av valutan kostar i sek
            sek_val = 1 / rate

            rows.append(
                {
                    "date": pd.to_datetime(d),
                    "currency": curr,
                    "sek": round(sek_val, 4),
                }
            )

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values(["currency", "date"])

    return df


def group_by_time(df, period="Day"):
    if df.empty:
        return df

    df = df.copy()

    # gör om datumet beroende på vad man valt i dropdownen
    if period == "Week":
        df["period"] = df["date"].dt.strftime("%Y-W%W")
    elif period == "Month":
        df["period"] = df["date"].dt.strftime("%Y-%m")
    elif period == "Quarter":
        year = df["date"].dt.year.astype(str)
        quarter = df["date"].dt.quarter.astype(str)
        df["period"] = year + "-Q" + quarter
    else:
        df["period"] = df["date"].dt.strftime("%Y-%m-%d")

    # gruppera och räkna ut medelvärde för perioden
    grouped = df.groupby(["currency", "period"])["sek"].mean().reset_index()
    grouped["sek"] = grouped["sek"].round(4)
    grouped = grouped.rename(columns={"period": "date"})

    return grouped


def calc_percent(df):
    if df.empty:
        return df

    df = df.copy()

    # ny kolumn med procentuell förändring
    df["pct_change"] = df.groupby("currency")["sek"].pct_change() * 100
    df["pct_change"] = df["pct_change"].fillna(0).round(2)

    return df


def get_table_data(df):
    if df.empty:
        return []

    table_rows = []

    # går igenom varje valuta och tar fram min, max och förändring
    for curr, group in df.groupby("currency"):
        first_val = group["sek"].iloc[0]
        last_val = group["sek"].iloc[-1]
        max_val = group["sek"].max()
        min_val = group["sek"].min()
        last_date = group["date"].iloc[-1].strftime("%Y-%m-%d")

        # förändring i procent från start till slut
        change_pct = ((last_val - first_val) / first_val) * 100

        table_rows.append(
            {
                "currency": curr,
                "latest_sek": round(last_val, 4),
                "max_sek": round(max_val, 4),
                "min_sek": round(min_val, 4),
                "change_12m": round(change_pct, 2),
                "date": last_date,
            }
        )

    return table_rows


def get_answers(df):
    if df.empty:
        return {}

    table = get_table_data(df)

    eur_pct = None
    best_curr = table[0]
    worst_curr = table[0]
    highest_curr = table[0]

    for row in table:
        # hur har eur förändrats
        if row["currency"] == "EUR":
            eur_pct = row["change_12m"]

        # vilken har stärkts och försvagats mest
        if row["change_12m"] > best_curr["change_12m"]:
            best_curr = row
        if row["change_12m"] < worst_curr["change_12m"]:
            worst_curr = row

        # vilken har haft högst kurs
        if row["max_sek"] > highest_curr["max_sek"]:
            highest_curr = row

    return {
        "eur_change": eur_pct,
        "strongest": best_curr["currency"],
        "strongest_pct": best_curr["change_12m"],
        "weakest": worst_curr["currency"],
        "weakest_pct": worst_curr["change_12m"],
        "highest": highest_curr["currency"],
        "highest_sek": highest_curr["max_sek"],
    }


def convert_to_sek(amount, currency, latest_data):
    if not latest_data:
        return None

    rate = None
    rate_date = ""

    for row in latest_data:
        if row["quote"] == currency:
            rate = row["rate"]
            rate_date = row["date"]

    if not rate:
        return None

    # räknar om beloppet till sek
    one_in_sek = 1 / rate
    total_sek = amount * one_in_sek

    return {
        "amount": amount,
        "currency": currency,
        "sek_amount": round(total_sek, 2),
        "rate": round(one_in_sek, 4),
        "date": rate_date,
    }
