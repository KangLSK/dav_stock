import streamlit as st
import datetime
import pandas as pd
from src.data_loader import get_stock_price, load_financial_statements, load_month_revenue
from src.indicators import add_ma
from src.charting import kline_with_ma, volume_bar_chart
from src.fundamentals.analysis import analyze_financials
#from src.gpt_summary import summary

# 預設日期範圍為一年
TODAY = datetime.date.today()
ONE_YEAR_AGO = TODAY - datetime.timedelta(days=365)

st.set_page_config("台股即時分析", layout="wide")
st.sidebar.title("輸入參數")
stock_id = st.sidebar.text_input("股票代號", "2330")
start = st.sidebar.date_input("開始日", value=ONE_YEAR_AGO)
end   = st.sidebar.date_input("結束日", value=TODAY)
show_gpt = st.sidebar.checkbox("顯示 AI 摘要", value=True)

tab1, tab2 = st.tabs(["技術分析", "基本面分析"])

with tab1:
    if st.button("載入技術資料"):
        df = get_stock_price(stock_id, start, end)
        df = add_ma(df)
        st.plotly_chart(kline_with_ma(df), use_container_width=True)
        st.plotly_chart(volume_bar_chart(df), use_container_width=True)
        # if show_gpt:
        #     st.success(summary(df, stock_id))

with tab2:
    # --- 基本面（財報） ---
    df_fs = load_financial_statements(stock_id, str(start))
    if df_fs.empty:
        st.warning("財報資料為空，請檢查代號或日期。")
    else:
        all_dates = df_fs["date"].sort_values(ascending=False).unique()
        max_quarters = len(all_dates)
        # 預設季報長度為4
        default_quarters = 4 if max_quarters >= 4 else max_quarters
        # 只有當使用者調整了日期範圍，才允許更改季數
        date_changed = (start != ONE_YEAR_AGO or end != TODAY)
        num_quarters = st.sidebar.number_input(
            "顯示最近幾季財報",
            min_value=1,
            max_value=max_quarters,
            value=default_quarters,
            step=1,
            disabled=not date_changed
        )
        if not date_changed and num_quarters != default_quarters:
            st.info("請先更動日期範圍，才能調整季報長度。")
        if num_quarters > max_quarters:
            st.warning(f"超過可用季數，最多僅有 {max_quarters} 季。")
            num_quarters = max_quarters
        selected_dates = all_dates[:num_quarters]
        df_recent = df_fs[df_fs["date"].isin(selected_dates)]

        # 依季度分組顯示
        for q_date in selected_dates:
            df_q = df_recent[df_recent["date"] == q_date]
            wide = df_q.pivot(
                index=["date", "stock_id"],
                columns="type",
                values="value"
            ).reset_index()
            record = wide.to_dict("records")[0] if len(wide) > 0 else None
            # 取得季別字串（如 2020-Q1）
            quarter_str = f"{q_date.year}-Q{((q_date.month-1)//3)+1}"
            with st.expander(f"{quarter_str} 季財報明細"):
                st.markdown(f"### {quarter_str}")
                # 以條列式顯示財報科目與金額，單位為萬，負數加*，不顯示萬以下
                for _, row in df_q.iterrows():
                    name = row["origin_name"]
                    value = row["value"]
                    if pd.isnull(value):
                        continue
                    value_wan = int(value) // 10000
                    if abs(value_wan) < 1:
                        continue
                    # 保留負號，負數科目加*
                    if int(value) < 0:
                        name = f"*{name}"
                        value_fmt = f"{value_wan:,}萬"  # value_wan 本身有負號
                    else:
                        value_fmt = f"{value_wan:,}萬"
                    st.write(f"**{name}**：{value_fmt}")
            if record:
                analysis = analyze_financials(record)
                if analysis:
                    st.subheader(f"{quarter_str} 基本面分析結果")
                    st.json(analysis)

    # --- 月營收 ---
    if st.button("顯示月營收", key="btn_rev"):
        df_revenue = load_month_revenue(stock_id, str(start))
        if df_revenue.empty:
            st.warning("月營收資料為空，請檢查代號或日期。")
        else:
            st.subheader("月營收")
            from src.charting import revenue_bar_line_chart
            st.plotly_chart(revenue_bar_line_chart(df_revenue), use_container_width=True)
            df_revenue_display = df_revenue.copy()
            df_revenue_display["date"] = pd.to_datetime(df_revenue_display["date"]).dt.strftime("%Y-%m")
            st.dataframe(
                df_revenue_display[["date", "revenue"]],
                use_container_width=True
            )
