import pandas as pd


def build_df(data, selected):
    """Convert API data into a DataFrame for selected currencies."""
    if not data:
        return pd.DataFrame()

    rows = []
    for row in data:
        d = row["date"]
        curr = row["quote"]
        rate = row["rate"]

        if curr in selected:
            # Store the value of 1 SEK in the selected currency
            sek_val = rate

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
    """Group exchange rates by day, week, month or quarter."""
    if df.empty:
        return df

    df = df.copy()

    # Format dates based on the selected period
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

    # Group by currency and period, then calculate average rates
    grouped = df.groupby(["currency", "period"])["sek"].mean().reset_index()
    grouped["sek"] = grouped["sek"].round(4)
    grouped = grouped.rename(columns={"period": "date"})

    return grouped


def calc_percent(df):
    """Calculate percentage changes between consecutive exchange rates."""
    if df.empty:
        return df

    df = df.copy()

    # Add a new column with percentage changes for each currency
    df["pct_change"] = df.groupby("currency")["sek"].pct_change() * 100
    df["pct_change"] = df["pct_change"].fillna(0).round(2)

    return df


def get_table_data(df):
    """Calculate statistics and percentage changes for each currency."""
    if df.empty:
        return []

    table_rows = []

    # Calculate statistics for each currency
    for curr, group in df.groupby("currency"):
        first_val = group["sek"].iloc[0]
        last_val = group["sek"].iloc[-1]
        max_val = group["sek"].max()
        min_val = group["sek"].min()
        last_date = group["date"].iloc[-1].strftime("%Y-%m-%d")

        # Calculate percentage change from the first to the last rate
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
