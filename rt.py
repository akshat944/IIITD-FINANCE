from yahoo_fin import stock_info as si
from yahoo_fin import news

web = 14
country = 13
info = 5


def realtime(stock):
    return round(si.get_live_price(stock), 2)


def detail(stock):
    df = si.get_company_info(stock)
    return df.values[info][0], df.values[country][0], df.values[web][0]
