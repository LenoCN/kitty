from tokenize import endpats
import backtrader as bt

from strategy.kitty_strategy import kitty_strategy
from strategy.kitty_strategy2 import kitty_strategy2
from strategy.kitty_strategy3 import kitty_strategy3
from strategy.boll_strategy import  boll_strategy
from kittytools.get_ths_daily import get_ths_daily
from kittytools.get_daily import get_daily
from kittytools.feeds_tushare import feeds_tushare
from kittytools.add_boll import add_boll
from kittytools.add_trend_factor import add_trend_factor

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    #获取数据
    #start_date = [2021, 6, 2]
    #end_date = [2022, 6 , 16]
    start_date = [2014, 5, 6]
    end_date = [2022, 6 , 16]
    start_date_str = str(start_date[0]) + str('%02d' %start_date[1]) + str('%02d' %start_date[2])
    end_date_str = str(end_date[0]) + str('%02d' %end_date[1]) + str('%02d' %end_date[2])

    #ts_code = '885922.TI' #盐湖提锂
    ts_code = '885545.TI' #

    df = get_ths_daily(ts_code, start_date_str, end_date_str)
    #df = get_daily(ts_code, start_date_str, end_date_str)
    df = add_boll(df)
    df = add_trend_factor(df, time_period=20, trend_top_coef=0.5, trend_top=1, plot_en=False)

    #df = df[['trade_date','close','open','high','low','vol']]
    #print(start_date_str, end_date_str)
    data = feeds_tushare(df, start_date, end_date)

    cerebro.adddata(data)  # 将数据传入回测系统
    #cerebro.addstrategy(kitty_strategy)  # 将数据传入回测系统
    #cerebro.addstrategy(kitty_strategy2)  # 将数据传入回测系统
    cerebro.addstrategy(kitty_strategy3)  # 将数据传入回测系统
    #cerebro.addstrategy(boll_strategy)  # 将数据传入回测系统
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0000)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot() 