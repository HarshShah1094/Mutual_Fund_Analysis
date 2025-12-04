from datetime import datetime
from collections import defaultdict
import pandas as pd


def read_nav_data(csv_path):
    df = pd.read_csv(csv_path)
    required_cols = {"Fund Name", "Date", "NAV"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df = df.rename(
        columns={
            "Fund Name": "fund",
            "Date": "date",
            "NAV": "nav",
        }
    )

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    invalid_rows = df[df["date"].isna() | df["nav"].isna()]
    if not invalid_rows.empty:
        print(f"Skipping {len(invalid_rows)} invalid rows due to bad date/NAV values.")
        df = df.dropna(subset=["date", "nav"])

    df["date"] = df["date"].apply(lambda ts: ts.to_pydatetime())

    return df[["fund", "date", "nav"]].to_dict("records")


def group_by_fund(records):
    grouped = defaultdict(list)
    for r in records:
        grouped[r["fund"]].append(r)

    for recs in grouped.values():
        recs.sort(key=lambda r: r["date"])

    return grouped

def compute_cagr(begin_nav, end_nav, years):
    if begin_nav <= 0 or end_nav <= 0 or years <= 0:
        raise ValueError("NAVs and years must be positive")
    return (end_nav / begin_nav) ** (1.0 / years) - 1.0


def compute_7yr_cagr_per_fund(grouped, years=7.0):
    cagr_by_fund = {}

    for fund, recs in grouped.items():
        if len(recs) < 2:
            continue

        begin_nav = recs[0]["nav"]
        end_nav = recs[-1]["nav"]

        try:
            cagr_by_fund[fund] = compute_cagr(begin_nav, end_nav, years)
        except ValueError:
            continue

    return cagr_by_fund


def get_top_n_funds(cagr_by_fund, n):
    return sorted(cagr_by_fund.items(), key=lambda kv: kv[1], reverse=True)[:n]

def get_bottom_n_funds(cagr_by_fund, n):
    return sorted(cagr_by_fund.items(), key=lambda kv: kv[1])[:n]

def detect_nav_swings(grouped, threshold_pct=5.0):
    swings = []

    for fund, recs in grouped.items():
        # recs already sorted by date in group_by_fund()
        for prev, curr in zip(recs, recs[1:]):
            if prev["nav"] == 0:
                continue
            pct_change = ((curr["nav"] - prev["nav"]) / prev["nav"]) * 100.0
            if abs(pct_change) > threshold_pct:
                swings.append((fund, curr["date"], pct_change))

    return swings

def print_cagr_results(cagr_by_fund):
    if not cagr_by_fund:
        print("No CAGR data available.")
        return

    top_2 = get_top_n_funds(cagr_by_fund, 2)
    bottom_2 = get_bottom_n_funds(cagr_by_fund, 2)

    print("\n=== Top 2 Funds by 7-Year CAGR ===")
    for fund, cagr in top_2:
        print(f"{fund:40s} CAGR: {cagr * 100:7.2f}%")

    print("\n=== Bottom 2 Funds by 7-Year CAGR ===")
    for fund, cagr in bottom_2:
        print(f"{fund:40s} CAGR: {cagr * 100:7.2f}%")


def print_nav_swings(swings):
    if not swings:
        print("\nNo NAV swings greater than ±5% were detected.")
        return

    print("\n=== NAV Swings > ±5% ===")
    print(f"{'Fund Name':40s} {'Date':12s} {'Change (%)':>12s}")
    print("-" * 70)
    for fund, date, pct_change in swings:
        date_str = date.strftime("%d-%m-%Y")
        print(f"{fund:40s} {date_str:12s} {pct_change:12.2f}")

def main():
    csv_path = input("Enter path to NAV CSV file (e.g. MF1.csv): ").strip()
    try:
        records = read_nav_data(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    if not records:
        print("No valid NAV records found.")
        return

    grouped = group_by_fund(records)

    cagr_by_fund = compute_7yr_cagr_per_fund(grouped, years=7.0)
    print_cagr_results(cagr_by_fund)

    swings = detect_nav_swings(grouped, threshold_pct=5.0)
    print_nav_swings(swings)

if __name__ == "__main__":
    main()
