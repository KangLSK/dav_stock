# 月營收折線圖
def revenue_line_chart(df):
    import plotly.express as px
    fig = px.line(
        df.sort_values("date"),
        x="date",
        y="revenue",
        title="月營收折線圖",
        markers=True,
        labels={"date": "日期", "revenue": "營收"}
    )
    fig.update_layout(xaxis_title="日期", yaxis_title="營收", title_x=0.5)
    return fig
# 月營收 bar chart
import plotly.express as px
def revenue_bar_chart(df):
    # df 需包含 date, revenue 欄位
    fig = px.bar(
        df.sort_values("date"),
        x="date",
        y="revenue",
        title="月營收 Bar Chart",
        labels={"date": "日期", "revenue": "營收"}
    )
    fig.update_layout(xaxis_title="日期", yaxis_title="營收", title_x=0.5)
    return fig
import plotly.graph_objects as go

def kline_with_ma(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['date'], open=df['open'], high=df['max'],
        low=df['min'], close=df['close'],
        increasing_line_color='red',   # 上漲紅色
        decreasing_line_color='green', # 下跌綠色
        name='K'))
    if 'MA5' in df:
        fig.add_trace(go.Scatter(x=df['date'], y=df['MA5'], line=dict(color='blue'), name='MA5'))
    if 'MA20' in df:
        fig.add_trace(go.Scatter(x=df['date'], y=df['MA20'], line=dict(color='orange'), name='MA20'))
    if 'MA60' in df:
        fig.add_trace(go.Scatter(x=df['date'], y=df['MA60'], line=dict(color='purple'), name='MA60'))

    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig
def volume_bar_chart(df):
    # 根據漲跌決定顏色
    colors = ['red' if c >= o else 'green' for c, o in zip(df['close'], df['open'])]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['Trading_Volume'],
        marker_color=colors,
        name='成交量'
    ))
    fig.update_layout(
        xaxis_title='日期',
        yaxis_title='成交量',
        template='plotly_white'
    )
    return fig
# 月營收 Bar+Line Chart

def revenue_bar_line_chart(df):
    import plotly.graph_objects as go
    import pandas as pd
    df_sorted = df.sort_values("date").copy()
    # 將 date 轉成字串格式（只顯示年月）
    df_sorted["date_str"] = pd.to_datetime(df_sorted["date"]).dt.strftime("%Y-%m")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted["date_str"],
        y=df_sorted["revenue"],
        marker_color="rgba(0,123,255,0.5)",
        name="月營收 Bar",
        #hovertemplate="日期: %{x}<br>營收: %{y:,}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=df_sorted["date_str"],
        y=df_sorted["revenue"],
        name="月營收 Line",
        mode="lines+markers",
        line=dict(color="orange", width=2),
        marker=dict(size=6),
        #hovertemplate="日期: %{x}<br>營收: %{y:,}<extra></extra>"
    ))
    fig.update_layout(
        title="月營收 ",
        xaxis_title="日期",
        yaxis_title="營收",
        title_x=0.5,
        xaxis=dict(type="category")
    )
    return fig
