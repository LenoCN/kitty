import backtrader as bt
 
class kitty_strategy2(bt.Strategy):
    #自定义参数，每次买入100手
    params=(('size',1000),)
    def __init__(self):
        self.dataclose=self.datas[0].close
        self.low=self.datas[0].low
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
            if  self.lines.value_rate[0] > 0.55 and self.lines.value_rate[0] < 0.9:
                if self.low[0] < self.dataclose[-1] and self.dataclose[0]/self.low[0] > 1.02:
                    self.order=self.buy(size= 0.9 * (self.broker.getcash() // self.dataclose))
                    self.buyprice = self.dataclose[0]
                elif self.lines.value_rate[-1] < self.lines.value_rate[0] and self.dataclose[0]/self.dataclose[-1] > 1.02:
                    self.order=self.buy(size= 0.9 * (self.broker.getcash() // self.dataclose))
                    self.buyprice = self.dataclose[0]
        else:
            if self.lines.value_rate[0] >= 0.9:
                self.order=self.sell(size=self.broker.getposition(self.data).size)
                self.yield_rate.append(self.dataclose[0] / self.buyprice)
            elif (self.dataclose - self.broker.getposition(self.data).price)/self.broker.getposition(self.data).price < -0.07:
                self.order=self.sell(size=self.broker.getposition(self.data).size)
                self.yield_rate.append(self.dataclose[0] / self.buyprice)

    def stop(self):
        fh = open('tmp_list','a')
        for i in self.yield_rate:
         fh.write(str(i)+'\n')
        fh.close()
