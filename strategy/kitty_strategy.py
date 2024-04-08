import backtrader as bt
 
class kitty_strategy(bt.Strategy):
    #自定义参数，每次买入100手
    params=(('size',1000),)
    def __init__(self):
        self.dataclose=self.datas[0].close
        self.order=None
        self.buyprice=None
        self.buycomm=None
        self.yield_rate = []
        ##使用自带的indicators中自带的函数计算出支撑线和压力线，period设置周期，默认是20
        self.lines.top=bt.indicators.BollingerBands(self.datas[0],period=20).top
        self.lines.bot=bt.indicators.BollingerBands(self.datas[0],period=20).bot
        self.lines.value_rate = (self.dataclose - self.lines.bot) / (self.lines.top - self.lines.bot)

    def next(self):
        if not self.position:
            if self.dataclose>=self.lines.bot[0]:
                if self.lines.value_rate[-1] <= 0.03 and self.lines.value_rate[0] >= 0.07:
                    self.order=self.buy(size= 0.9 * (self.broker.getcash() // self.dataclose))
                    self.buyprice = self.dataclose[0]
                #elif self.lines.value_rate[-1] <= 0.53 and self.lines.value_rate[0] >= 0.57:
                #    self.order=self.buy(size=(self.broker.getcash() // self.dataclose))
        else:
            if self.lines.value_rate[0] >= 0.97:
                self.order=self.sell(size=self.broker.getposition(self.data).size)
                self.yield_rate.append(self.dataclose[0] / self.buyprice)
            elif (self.dataclose - self.broker.getposition(self.data).price)/self.broker.getposition(self.data).price < -0.07:
                self.order=self.sell(size=self.broker.getposition(self.data).size)
                self.yield_rate.append(self.dataclose[0] / self.buyprice)

    def stop(self):
        print(self.yield_rate)
