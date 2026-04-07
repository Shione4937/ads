import pandas as pd
import os
import calendar
from datetime import date

DATA_DIR = os.path.dirname(__file__)
TODAY = date(2026, 4, 14)


def load_demo(client=None, date_from=None, date_to=None):
    path = os.path.join(DATA_DIR, "demo_data.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    if client:
        df = df[df["client"] == client]
    if date_from:
        df = df[df["date"] >= pd.to_datetime(date_from).date()]
    if date_to:
        df = df[df["date"] <= pd.to_datetime(date_to).date()]
    return df


def get_clients():
    path = os.path.join(DATA_DIR, "demo_data.csv")
    df = pd.read_csv(path, usecols=["client"])
    return sorted(df["client"].unique().tolist())


def get_summary(df):
    summary = (
        df.groupby("platform")
        .agg(cost=("cost","sum"), imp=("imp","sum"), click=("click","sum"),
             cv=("cv","sum"), budget=("budget_monthly","first"), target_cpa=("target_cpa","first"))
        .reset_index()
    )
    summary["ctr"] = (summary["click"] / summary["imp"].replace(0,1) * 100).round(2)
    summary["cpc"] = (summary["cost"] / summary["click"].replace(0,1)).round(0)
    summary["cpa"] = (summary["cost"] / summary["cv"].replace(0,1)).round(0)
    meta_mask = summary["platform"] == "meta"
    summary.loc[meta_mask, "cv"] = 0
    summary.loc[meta_mask, "cpa"] = None
    return summary


def get_budget_progress(client):
    month_start = date(TODAY.year, TODAY.month, 1)
    df = load_demo(client=client, date_from=str(month_start), date_to=str(TODAY))
    days_elapsed = (TODAY - month_start).days + 1
    days_in_month = calendar.monthrange(TODAY.year, TODAY.month)[1]
    days_remaining = days_in_month - days_elapsed

    rows = []
    for platform in ["google", "yahoo", "meta", "tiktok"]:
        pf = df[df["platform"] == platform]
        cost_used = pf["cost"].sum()
        budget = pf["budget_monthly"].iloc[0] if len(pf) > 0 else 0
        remaining = budget - cost_used
        daily_pace = cost_used / days_elapsed if days_elapsed > 0 else 0
        projected = cost_used + daily_pace * days_remaining
        per_day_target = remaining / days_remaining if days_remaining > 0 else 0
        rows.append({
            "platform": platform,
            "budget": budget,
            "cost_used": round(cost_used),
            "remaining": round(remaining),
            "pct_used": round(cost_used / budget * 100, 1) if budget > 0 else 0,
            "daily_pace": round(daily_pace),
            "per_day_target": round(per_day_target),
            "projected": round(projected),
            "days_elapsed": days_elapsed,
            "days_remaining": days_remaining,
            "days_in_month": days_in_month,
        })
    return pd.DataFrame(rows)


def get_monthly_trend(df):
    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return (
        df.groupby("month")
        .agg(cost=("cost","sum"), imp=("imp","sum"), click=("click","sum"), cv=("cv","sum"))
        .reset_index()
    )
