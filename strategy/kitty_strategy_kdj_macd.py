import backtrader as bt
 
class boll_strategy(bt.Strategy):
    #自定义参数，每次买入100手
    params=(('size',10),)
    def __init__(self):
        self.dataclose=self.datas[0].close
        self.order=None
        self.buyprice=None
        self.buycomm=None
        ##使用自带的indicators中自带的函数计算出支撑线和压力线，period设置周期，默认是20
        self.lines.top=bt.indicators.BollingerBands(self.datas[0],period=20).top
        self.lines.bot=bt.indicators.BollingerBands(self.datas[0],period=20).bot
    def next(self):
        if not self.position:
            if self.dataclose<=self.lines.bot[0]:
                #执行买入
                #self.order=self.buy(size=self.params.size)
                self.order=self.buy(size=(0.9 * self.broker.getcash() // self.dataclose))
        else:
            if self.dataclose>=self.lines.top[0]:
                #执行卖出
                #self.order=self.sell(size=self.params.size)
                self.order=self.sell(size=self.broker.getposition(self.data).size)
