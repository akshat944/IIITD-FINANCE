import yfinance as yf
import plotly.graph_objs as go
from yahoo_fin import stock_info as si
from yahoo_fin import news
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from rt import realtime
from cnd import candles
from cnd import candlem
from cnd import news_s
from cnd import newsxs
from rt import detail
import os
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure, show, output_file
import random
from datetime import datetime, timedelta, date, time
from bokeh.layouts import row
import plotly.graph_objs as go
import json
import plotly

suma = list()
tit = list()
lnk = list()

ve = dict(si.get_day_most_active())
xxx = list(ve.values())
rcliss = list(xxx[0][0:20])
aclis = list(xxx[0][0:5])

gain = dict(si.get_day_gainers())
xg = list(gain.values())
galis = list(xg[1][0:5])

los = dict(si.get_day_losers(20))
xl = list(los.values())
lalis = list(xl[1][0:5])

stock = list()
stock_gain = si.get_day_gainers()
stock_low = si.get_day_losers(20)
stock_active = si.get_day_most_active()

stock = (
    stock_gain["Symbol"].tolist()
    + stock_active["Symbol"].tolist() + stock_low["Symbol"].tolist()
)
stock = list(set(stock))

app = Flask(__name__)

nlis = list()

picfolder = os.path.join("static", "pics")
app.config["UPLOAD_FOLDER"] = picfolder


@app.route("/")
def home():

    del nlis[:]

    for i in range(38):
        rs = random.choice(stock)
        nlis.append(rs)

    cclis = ["High Low Difference", "Moving Average", "Daily Returns"]

    logo = os.path.join(app.config["UPLOAD_FOLDER"], "IIITD_fin.png")
    from yahoo_fin import news

    for x in aclis:
        x = dict(news.get_yf_rss(x)[0:1][0])
        xx = list(x.values())
        suma.append(xx[0])  # summary
        tit.append(xx[8])  # title
        lnk.append(xx[5])  # link

    rck = random.choice(rcliss)

    xc = candles(rck)
    # fig.show()
    return render_template(
        "home.html",
        suma=suma,
        tit=tit,
        lnk=lnk,
        logo=logo,
        graphJSON=xc,
        stock=stock,
        cclis=cclis,
        nlen=len(stock),
        nlis=nlis,
    )


def plot_differentPrices(df):
    from datetime import datetime as dt

    x_high = df["High"]
    x_close = df["Low"]
    y = df["Date"]

    func1 = [y, x_high, x_close]

    return func1


def moving_average(df):

    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure
    from datetime import datetime as dt

    Moving_AVG_1yr_10days = []
    y = []
    qu = []
    cnt = 10
    for i in df.index:
        if cnt > 0:
            qu.append(int(df["Open"][i]))
            cnt -= 1
        else:
            qu.append(int(df["Open"][i]))
            qu.pop(0)
            Moving_AVG_1yr_10days.append(sum(qu) / 10)
            y.append(df["Date"][i])

    func2 = [y, Moving_AVG_1yr_10days]

    return func2


max_return = []


def daily_max_return(low, high):
    for i in range(0, len(low)):
        max_return.append(high[i] - low[i])

    return max_return


def plot_dailyReturn(df):

    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure
    from datetime import datetime as dt

    x_close = df["Close"]
    x_open = df["Open"]
    x = x_close - x_open
    y = df["Date"]

    func3 = [y, x]

    return func3


@app.route("/dataset", methods=["POST"])
def dataset():
    stock = request.form["stk"]
    c = candles(stock)
    df = yf.download(tickers=stock, period="max", interval="1d")
    df = df.reset_index()

    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure
    from bokeh.plotting import row

    out1 = plot_differentPrices(df)
    out2 = moving_average(df)
    out3 = plot_dailyReturn(df)

    graph1 = figure(
        title="Bokeh High,Low Graph",
        x_axis_type="datetime",
        y_axis_label="Stock Value in USD.",
        x_axis_label="Time",
    )
    graph1.multi_line([out1[1], out1[2]], color=["firebrick", "navy"])

    graph1.line(out1[0], out1[1], color="red", legend_label="Low Stock")
    graph1.line(out1[0], out1[2], color="yellow", legend_label="High Stock")
    graph1.legend.location = "top_left"
    graph1.legend.title = "Company : " + stock
    graph1.legend.title_text_font_style = "bold"

    graph2 = figure(
        title="Bokeh Daily Return Graph",
        x_axis_type="datetime",
        y_axis_label="Daily Return Stock Value in USD.",
        x_axis_label="Time",
    )

    graph2.line(out3[0], out3[1], color="red", legend_label="Daily Return")
    graph2.legend.location = "top_left"
    graph2.legend.title = "Company : " + stock
    graph2.legend.title_text_font_style = "bold"

    graph3 = figure(
        title="Moving Average",
        x_axis_type="datetime",
        y_axis_label="Moving Average Stock Value in USD.",
        x_axis_label="Time",
    )
    graph3.line(out2[0], out2[1], legend_label="Moving Average")
    graph3.legend.location = "top_left"
    graph3.legend.title = "Company : " + stock
    graph3.legend.title_text_font_style = "bold"

    cdn_js = CDN.js_files
    script1, div1 = components(graph1)
    script2, div2 = components(graph2)
    script3, div3 = components(graph3)

    return render_template(
        "plot2.html",
        script1=script1,
        div1=div1,
        cdn_js=cdn_js,
        script2=script2,
        div2=div2,
        script3=script3,
        div3=div3,
        graphJSON=c,
    )


@app.route("/comp", methods=["POST", "GET"])
def comp():
    stock1 = request.form["stock1"]
    stock2 = request.form["stock2"]
    a = candlem(stock1)
    b = candlem(stock2)
    gpt = request.form["graph_type"]

    df1 = yf.download(tickers=stock1, period="max", interval="1d")
    df1 = df1.reset_index()  # df1
    df2 = yf.download(tickers=stock2, period="max", interval="1d")
    df2 = df2.reset_index()  # df2

    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure, curdoc
    from bokeh.driving import count

    data1 = []
    data2 = []

    if gpt == "High Low Difference":
        data1 = plot_differentPrices(df1)
        data2 = plot_differentPrices(df2)

        gp1 = figure(
            title="Bokeh High,Low Comparision Graph",
            x_axis_type="datetime",
            y_axis_label="Stock Value in USD.",
            x_axis_label="Time",
        )
        gp1.multi_line([data1[1], data1[2]], color=["firebrick", "navy"])

        gp1.line(data1[0], data1[1], color="red", legend_label="Low Stock")
        gp1.line(data1[0], data1[2], color="yellow", legend_label="High Stock")

        gp1.legend.location = "top_left"
        gp1.legend.title = "Company : " + stock1
        gp1.legend.title_text_font_style = "bold"

        gp2 = figure(
            title="Bokeh High,Low Comparision Graph",
            x_axis_type="datetime",
            y_axis_label="Stock Value in USD.",
            x_axis_label="Time",
        )
        gp2.multi_line([data2[1], data2[2]], color=["firebrick", "navy"])

        gp2.line(data2[0], data2[1], color="red", legend_label="Low Stock")
        gp2.line(data2[0], data2[2], color="yellow", legend_label="High Stock")

        gp2.legend.location = "top_left"
        gp2.legend.title = "Company : " + stock2
        gp2.legend.title_text_font_style = "bold"

        cdn_js = CDN.js_files
        script1, div1 = components(gp1)
        script2, div2 = components(gp2)

        return render_template(
            "plot3.html",
            script1=script1,
            div1=div1,
            cdn_js=cdn_js,
            script2=script2,
            div2=div2,
            graph2JSON=b,
            graphJSON=a,
        )

    elif gpt == "Moving Average":
        data1 = moving_average(df1)
        data2 = moving_average(df2)

        gp11 = figure(
            title="Moving Average",
            x_axis_type="datetime",
            y_axis_label="Moving Average of Stock in USD.",
            x_axis_label="Time",
        )
        gp11.line(data1[0], data1[1], legend_label="Moving Average")

        gp11.legend.location = "top_left"
        gp11.legend.title = "Company : " + stock1
        gp11.legend.title_text_font_style = "bold"

        gp22 = figure(
            title="Moving Average",
            x_axis_type="datetime",
            y_axis_label="Moving Average of Stock in USD.",
            x_axis_label="Time",
        )
        gp22.line(data2[0], data2[1], legend_label="Moving Average")

        gp22.legend.location = "top_left"
        gp22.legend.title = "Company : " + stock2
        gp22.legend.title_text_font_style = "bold"

        cdn_js = CDN.js_files
        script1, div1 = components(gp11)
        script2, div2 = components(gp22)

        return render_template(
            "plot3.html",
            script1=script1,
            div1=div1,
            cdn_js=cdn_js,
            script2=script2,
            div2=div2,
            graph2JSON=b,
            graphJSON=a,
        )

    elif gpt == "Daily Returns":
        data1 = plot_dailyReturn(df1)
        data2 = plot_dailyReturn(df2)

        gp111 = figure(
            title="Bokeh Daily Return Graph",
            x_axis_type="datetime",
            y_axis_label="Daily Return in USD.",
            x_axis_label="Time",
        )

        gp111.line(data1[0], data1[1], color="red", legend_label="Daily Return")

        gp111.legend.location = "top_left"
        gp111.legend.title = "Company : " + stock1
        gp111.legend.title_text_font_style = "bold"

        gp222 = figure(
            title="Bokeh Daily Return Graph",
            x_axis_type="datetime",
            y_axis_label="Daily Return in USD.",
            x_axis_label="Time",
        )

        gp222.line(data2[0], data2[1], color="red", legend_label="Daily Return")

        gp222.legend.location = "top_left"
        gp222.legend.title = "Company : " + stock2
        gp222.legend.title_text_font_style = "bold"

        cdn_js = CDN.js_files
        script1, div1 = components(gp111)
        script2, div2 = components(gp222)

        return render_template(
            "plot3.html",
            script1=script1,
            div1=div1,
            cdn_js=cdn_js,
            script2=script2,
            div2=div2,
            graph2JSON=b,
            graphJSON=a,
        )

    output_file("plot2.html")


@app.route("/top_gainer", methods=["POST", "GET"])
def top_gainer():

    gain = dict(si.get_day_gainers())
    xg = list(gain.values())
    sgalis = list(xg[0][0:10])
    galis = list(xg[1][0:10])

    return render_template("gain.html", galis=galis, glen=len(galis), sgalis=sgalis)


@app.route("/top_loser", methods=["POST", "GET"])
def top_loser():

    los = dict(si.get_day_losers(20))
    xl = list(los.values())
    slalis = list(xl[0][0:10])
    lalis = list(xl[1][0:10])

    return render_template("loser.html", lalis=lalis, llen=len(lalis), slalis=slalis)


@app.route("/max_gainer", methods=["POST", "GET"])
def max_gainer():

    gain = dict(si.get_day_gainers())
    xg = list(gain.values())
    sgalis = list(xg[0][0:50])
    galis = list(xg[1][0:50])

    return render_template("gain.html", galis=galis, glen=len(galis), sgalis=sgalis)


@app.route("/max_loser", methods=["POST", "GET"])
def max_loser():

    los = dict(si.get_day_losers(30))
    xl = list(los.values())
    slalis = list(xl[0][0:30])
    lalis = list(xl[1][0:30])

    return render_template("loser.html", lalis=lalis, llen=len(lalis), slalis=slalis)


@app.route("/details", methods=["POST", "GET"])
def details():
    stock = request.form["stk"]
    print(stock)
    rv = realtime(stock)
    xm = candlem(stock)
    # x = detail(stock)
    numm = 5
    nn = news_s(stock, numm)
    num=len(nn[0])
    return render_template(
        "detail.html", graphJSON=xm, nn=nn, rv=rv, nnl=num, stock=stock
    )


@app.route("/news", methods=["POST", "GET"])
def news():
    nn = newsxs(rcliss)
    return render_template("news.html", nn=nn)


if __name__ == "__main__":
    app.run(debug=True)