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
