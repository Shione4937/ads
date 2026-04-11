import pandas as pd
import os
import calendar
from datetime import date

DATA_DIR = os.path.dirname(__file__)
TODAY = date(2026, 4, 14)
ALL_CLIENTS = ["A社","B社","C社","D社","E社","F社","G社","H社"]
DEFAULT_SELECTED = ["A社","B社","C社","D社","E社"]


def load_demo(client=None, date_from=None, date_to=None):
    path = os.path.join(DATA_DIR, "demo_data.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    if client:
        if isinstance(client, list):
            df = df[df["client"].isin(client)]
        else:
            df = df[df["client"] == client]
    if date_from:
        df = df[df["date"] >= pd.to_datetime(date_from).date()]
    if date_to:
        df = df[df["date"] <= pd.to_datetime(date_to).date()]
    return df


def get_clients():
    return ALL_CLIENTS


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
    return summary


def get_all_clients_summary(clients, date_from, date_to):
    df = load_demo(client=clients, date_from=date_from, date_to=date_to)
    rows = []
    for client in clients:
        cdf = df[df["client"] == client]
        cost = cdf["cost"].sum()
        imp  = cdf["imp"].sum()
        click= cdf["click"].sum()
        cv   = cdf["cv"].sum()
        budget = cdf["budget_monthly"].iloc[0] if len(cdf) > 0 else 0
        target_cpa = cdf["target_cpa"].iloc[0] if len(cdf) > 0 else 0
        cpa  = round(cost / cv) if cv > 0 else None
        pct  = round(cost / budget * 100, 1) if budget > 0 else 0

        # アラート判定
        alerts = []
        if pct >= 90: alerts.append("予算90%超")
        if cpa and target_cpa and cpa > target_cpa * 1.5: alerts.append("CPA超過")

        rows.append({
            "client": client,
            "cost": round(cost),
            "imp": round(imp),
            "click": round(click),
            "cv": round(cv),
            "cpa": cpa,
            "budget": budget,
            "pct_used": pct,
            "target_cpa": target_cpa,
            "alerts": alerts,
        })
    return pd.DataFrame(rows)


def get_budget_progress(client):
    month_start = date(TODAY.year, TODAY.month, 1)
    df = load_demo(client=client, date_from=str(month_start), date_to=str(TODAY))
    days_elapsed = (TODAY - month_start).days + 1
    days_in_month = calendar.monthrange(TODAY.year, TODAY.month)[1]
    days_remaining = days_in_month - days_elapsed

    rows = []
    for platform in ["google","yahoo","meta","tiktok"]:
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


def get_calendar_html(year=None, month=None, today=None):
    """カレンダーHTML（今日ハイライト+残日数）を生成"""
    if today is None:
        today = TODAY
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    is_current_month = (year == today.year and month == today.month)
    days_in_month = calendar.monthrange(year, month)[1]
    first_weekday = date(year, month, 1).weekday()  # 0=月
    if is_current_month:
        elapsed = today.day
        remaining = days_in_month - elapsed + 1
        progress = round(elapsed / days_in_month * 100, 1)
    else:
        elapsed = days_in_month
        remaining = 0
        progress = 100.0

    month_names = {1:"1月",2:"2月",3:"3月",4:"4月",5:"5月",6:"6月",
                   7:"7月",8:"8月",9:"9月",10:"10月",11:"11月",12:"12月"}

    html = f'''
    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px;">
        <div style="text-align:center;font-weight:700;color:#1e1b4b;font-size:14px;margin-bottom:10px;">
            {year}年 {month_names[month]}
        </div>
        <table style="width:100%;text-align:center;font-size:12px;border-collapse:collapse;">
        <tr>'''
    for wd in ["月","火","水","木","金","土","日"]:
        color = "#dc2626" if wd == "日" else "#3b82f6" if wd == "土" else "#6b7280"
        html += f'<th style="color:{color};font-weight:600;padding:2px;">{wd}</th>'
    html += '</tr><tr>'

    for blank in range(first_weekday):
        html += '<td></td>'

    for d in range(1, days_in_month + 1):
        wd = (first_weekday + d - 1) % 7
        is_today = is_current_month and d == today.day
        past = (is_current_month and d < today.day) or not is_current_month

        if is_today:
            style = "background:#6366f1;color:#fff;border-radius:50%;font-weight:700;"
        elif past:
            style = "color:#1e1b4b;"
        else:
            style = "color:#94a3b8;"

        html += f'<td style="padding:3px;"><div style="{style}width:26px;height:26px;line-height:26px;margin:auto;font-size:11px;">{d}</div></td>'

        if wd == 6 and d < days_in_month:
            html += '</tr><tr>'

    html += '</tr></table>'
    if is_current_month:
        html += f'''
        <div style="display:flex;justify-content:space-between;margin-top:10px;font-size:11px;color:#6b7280;">
            <span>経過 <strong style="color:#1e1b4b;">{elapsed}日</strong></span>
            <span>残 <strong style="color:#1e1b4b;">{remaining}日</strong><span style="font-size:9px;color:#9ca3af;">（今日含む）</span></span>
            <span>進捗 <strong style="color:#6366f1;">{progress}%</strong></span>
        </div>'''
    html += '</div>'
    return html


def get_monthly_trend(df):
    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return (
        df.groupby("month")
        .agg(cost=("cost","sum"), imp=("imp","sum"), click=("click","sum"), cv=("cv","sum"))
        .reset_index()
    )
