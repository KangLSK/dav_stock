import plotly.graph_objects as go

def kline_with_ma(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['date'], open=df['open'], high=df['max'],
        low=df['min'], close=df['close'],
        name='K'))
    for m in [c for c in df.columns if c.startswith("MA")]:
        fig.add_trace(go.Scatter(
            x=df['date'], y=df[m], name=m, line=dict(width=1)))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig
