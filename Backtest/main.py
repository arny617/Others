# This is a sample Python script.
from strategy_2 import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def setup_backtest(data,strategy,cash=1000000.0):
    cerebro = bt.Cerebro(stdstats = False)
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.SizerFix, stake=100)
    cerebro.addstrategy(strategy)
    cerebro.broker.setcash(cash)
    #cerebro.broker.setcommission(commission=0.001)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.Value)
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.plot(iplot=False,volume=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from datetime import datetime
    from plotly.offline import plot
    import chart_studio.plotly as py
    import plotly.graph_objs as go
    import cufflinks as cf
    import matplotlib
    import matplotlib.pyplot as plt
    cf.go_offline()
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    from datafeed import *
    #init_notebook_mode(connected='true')
    import pandas as pd
    #import yfinance as yf
    import numpy as np
    bitcoin_data = bt.feeds.YahooFinanceData(dataname='BTC-USD',fromdate=datetime(2016,10, 3),todate=datetime(2020, 10, 28))
    filename = r"C:\Users\arnab\PycharmProjects\Backtest\BTC_USD.csv"
    # data = DataFeed(
    #     dataname=filename,
    #     fromdate=datetime(2016, 10, 3),
    #     todate=datetime(2020, 10, 28),
    #     dtformat=('%Y-%m-%d'),
    #     datetime=0,
    #     open=1,
    #     high=2,
    #     low=3,
    #     close=4,
    #     volume=-1,
    #     openinterest=-1)
    setup_backtest(bitcoin_data, SmaStrategy2, 1000000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
