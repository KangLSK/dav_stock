import os, pandas as pd, requests, streamlit as st

TOKEN = st.secrets["FINMIND_TOKEN"]
BASE = "https://api.finmindtrade.com/api/v4/data"


@st.cache_data(ttl=900)   # 15 min 快取
def get_stock_price(stock_id, start, end):
    params = dict(dataset="TaiwanStockPrice",
                  data_id=stock_id,
                  start_date=start,
                  end_date=end,
                  token=TOKEN)
    r = requests.get(BASE, params=params, timeout=10)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["data"])
    df["date"] = pd.to_datetime(df["date"])
    return df

def _fetch(dataset: str, stock_id: str, start_date: str | None = None) -> pd.DataFrame:
    params = {
        "dataset": dataset,
        "data_id": stock_id,
        "token": TOKEN,
    }
    if start_date:
        params["start_date"] = start_date

    r = requests.get(BASE, params=params, timeout=10)
    r.raise_for_status()
    js = r.json()
    return pd.DataFrame(js.get("data", []))


def load_financial_statements(stock_id: str, start_date: str | None = None) -> pd.DataFrame:
    """回傳欄位固定為 (date, stock_id, type, value, origin_name)"""
    df = _fetch("TaiwanStockFinancialStatements", stock_id, start_date)
    if df.empty:
        return df

    # 轉型
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # FinMind 原欄位: date / data_id / account / value / type(中文)
    rename_map = {
        "data_id": "stock_id",
        "account": "type",
        "type": "origin_name",  # 中文科目
    }
    if "origin_name" in df.columns:
        # FinMind 若已經有 origin_name 就不要覆蓋
        rename_map.pop("type", None)

    df = df.rename(columns=rename_map)
    keep_cols = ["date", "stock_id", "type", "value", "origin_name"]
    for col in keep_cols:
        if col not in df.columns:
            df[col] = None

    return df[keep_cols].sort_values("date", ascending=False).reset_index(drop=True)


def load_month_revenue(stock_id: str, start_date: str | None = None) -> pd.DataFrame:
    """回傳欄位固定為 (date, stock_id, country, revenue, revenue_month, revenue_year)"""
    df = _fetch("TaiwanStockMonthRevenue", stock_id, start_date)
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = ["revenue", "revenue_month", "revenue_year"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # FinMind 原欄位大致一致：date / data_id / country / revenue / revenue_month / revenue_year
    rename_map = {
        "data_id": "stock_id"
    }
    df = df.rename(columns=rename_map)

    keep_cols = ["date", "stock_id", "country", "revenue", "revenue_month", "revenue_year"]
    for col in keep_cols:
        if col not in df.columns:
            df[col] = None

    return df[keep_cols].sort_values("date", ascending=False).reset_index(drop=True)

