import yfinance as yf
import plotly.graph_objs as go
import json
import plotly
from yahoo_fin import news

def candles(stock):
    stock = str(stock)
    data = yf.download(tickers=stock, period="1d", interval="1m")
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="market data",
        )
    )
    fig.update_layout(
        title=str(stock) + " live share price evolution",
        yaxis_title="Stock Price (USD per Shares)",
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # fig.show()

    return graphJSON


def candlem(stock):
    stock = str(stock)
    data = yf.download(tickers=stock, period="max", interval="1d")
    data = data.reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="market data",
        )
    )
    fig.update_layout(
        title=str(stock) + " live share price evolution",
        yaxis_title="Stock Price (USD per Shares)",
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=5, label="5y", step="year", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=5, label="5m", step="month", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # fig.show()

    return graphJSON


def newsxs(stock):
    suma = list()
    tit = list()
    lnk = list()
    for x in stock:
        xn = dict(news.get_yf_rss(x)[0:1][0])
        xx = list(xn.values())
        suma.append(xx[0])  # summary
        tit.append(xx[8])  # title
        lnk.append(xx[5])  # link

    return suma, tit, lnk


def news_s(stock, num):
    suma = list()
    tit = list()
    lnk = list()
    x = news.get_yf_rss(stock)
    pl = len(x)
    if pl<num:
        for i in range(pl):
            x = news.get_yf_rss(stock)
            xx = list(x[i].values())
            suma.append(xx[0])  # summary
            tit.append(xx[8])  # title
            lnk.append(xx[5])  # link
    else:
        for i in range(num):
            x = news.get_yf_rss(stock)
            xx = list(x[i].values())
            suma.append(xx[0])  # summary
            tit.append(xx[8])  # title
            lnk.append(xx[5])  # link

    return suma, tit, lnk
