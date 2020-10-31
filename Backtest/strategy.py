### Backtest using strategy
import backtrader as bt
class SmaStrategy(bt.Strategy):
    params = (('slow_period', 20), ('fast_period', 10), ('rsi_period', 14),)

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.price = None
        self.comm = None
        self.slow_sma = bt.ind.SMA(self.datas[0], period=self.params.slow_period)
        self.fast_sma = bt.ind.SMA(self.datas[0], period=self.params.fast_period)
        self.rsi = bt.ind.RSI_SMA(self.datas[0], period=self.params.rsi_period)
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)
        self.pos = 0

    def log(self, txt):
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f'{dt}, {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.pos += 100
                self.log(f'BUY EXECUTED --- Price:{order.executed.price:.2f}, Cost: {order.executed.value:.2f}, \
                        Commission: {order.executed.comm:.2f},Position: {self.pos:.2f}')
                self.price = order.executed.price
                self.comm = order.executed.comm

            else:
                self.pos -= 100
                self.log(f'SELL EXECUTED --- Price:{order.executed.price:.2f}, Cost: {order.executed.value:.2f}, \
                    Commission: {order.executed.comm:.2f},Position: {self.pos:.2f}')

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Failed')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION RESULT --- Gross: {trade.pnl:.2f},Net: {trade.pnlcomm:.2f}')

    def next(self):
        if self.order:
            return
        if not self.position or self.pos==0:
            # if((self.fast_sma > self.slow_sma) and (self.rsi>50)):
            if (self.crossover > 0 and self.rsi > 50):
                self.log(f'BUY CREATED --- Price:{self.data_close[0]:.2f}')
                self.order = self.buy()
            elif (self.crossover < 0 and self.rsi < 50):
                self.log(f'SELL CREATED --- Price:{self.data_close[0]:.2f}')
                self.order = self.sell()
        else:
            if (self.pos > 0):
                # if((self.fast_sma < self.slow_sma) and (self.rsi<50)):
                if (self.crossover < 0 and self.rsi < 50):
                    self.log(f'SELL CREATED --- Price:{self.data_close[0]:.2f}')
                    self.order = self.sell()
                    self.order = self.sell()
            elif (self.pos < 0):
                if (self.crossover > 0 and self.rsi > 50):
                    self.log(f'BUY CREATED --- Price:{self.data_close[0]:.2f}')
                    self.order = self.buy()
                    self.order = self.buy()