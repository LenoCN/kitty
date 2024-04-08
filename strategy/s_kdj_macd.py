import backtrader as bt
 
class s_kdj_macd(bt.Strategy):
    #自定义参数，每次买入100手
    params=(('size',10),)
    def __init__(self):
        self.dataclose=self.datas[0].close
        self.k=self.datas[0].k
        self.d=self.datas[0].d
        self.j=self.datas[0].j
        self.kdj_jc=self.datas[0].kdj_jc
        self.macd_sc=self.datas[0].macd_sc
        self.order=None
        self.buyprice=None
        self.buycomm=None
        ##使用自带的indicators中自带的函数计算出支撑线和压力线，period设置周期，默认是20
        #self.lines.top=bt.indicators.BollingerBands(self.datas[0],period=20).top
        #self.lines.bot=bt.indicators.BollingerBands(self.datas[0],period=20).bot
        
        # 使用默认参数的MACD指标
        self.macd = bt.indicators.MACD()
    def next(self):
        if not self.position:
            if self.kdj_jc[0] == 1 and self.macd.macd[0] < 0:
                print(f'买入: {self.data.datetime.date(0)}')
                #执行买入
                #self.order=self.buy(size=self.params.size)
                self.order=self.buy(size=(0.9 * self.broker.getcash() // self.dataclose))
        # 当MACD线下穿信号线时，发生死叉
        elif self.macd_sc[0] == 1:
            self.sell(size=self.broker.getposition(self.data).size)
            print(f'卖出: {self.data.datetime.date(0)}')

    #def notify_order(self, order):
    #    if order.status in [order.Submitted, order.Accepted]:
    #        # 买卖单提交/接受，不做处理
    #        return

    #    if order.status in [order.Completed]:
    #        if order.isbuy():
    #            print(f'买入: {self.data.datetime.date(0)}, 价格: {order.executed.price}, 成本: {order.executed.value}, 手续费: {order.executed.comm}')
    #        elif order.issell():
    #            print(f'卖出: {self.data.datetime.date(0)}, 价格: {order.executed.price}, 成本: {order.executed.value}, 手续费: {order.executed.comm}')

    #    elif order.status in [order.Canceled, order.Margin, order.Rejected]:
    #        print(f'订单 {order.Status[order.status]}')