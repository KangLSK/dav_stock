import streamlit as st
import datetime
from src.data_loader import get_stock_price
from src.indicators import add_ma
from src.charting import kline_with_ma
#from src.gpt_summary import summary

st.set_page_config("台股即時分析", layout="wide")
st.sidebar.title("輸入參數")
stock_id = st.sidebar.text_input("股票代號", "2330")
start = st.sidebar.date_input("開始日", value=datetime.date(2024, 1, 1))
end   = st.sidebar.date_input("結束日")
show_gpt = st.sidebar.checkbox("顯示 AI 摘要", value=True)

if st.button("載入資料"):
    df = get_stock_price(stock_id, start, end)
    df = add_ma(df)
    st.plotly_chart(kline_with_ma(df), use_container_width=True)
    st.bar_chart(df.set_index("date")["Trading_Volume"])
    #if show_gpt:
       # st.success(summary(df, stock_id))
