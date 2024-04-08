import backtrader as bt
import pandas as pd
import tushare as ts
from strategy.boll_strategy import boll_strategy
from strategy.kitty_strategy import kitty_strategy
from strategy.kitty_strategy2 import kitty_strategy2
from kittytools.get_index_daily import get_index_daily
from kittytools.get_ths_daily import get_ths_daily
from kittytools.feeds_tushare import feeds_tushare
from kittytools.get_fund_basic import get_fund_basic
from kittytools.mysql import write_data,read_data

if __name__ == '__main__':

    df_fund_basic = get_fund_basic()
    print('Length of df_fund_basic : %d' % len(df_fund_basic))

    for i, ts_code in enumerate(df_fund_basic.ts_code):
        cerebro = bt.Cerebro()
        name = ts_code.split('.')[0] + 'DOT' + ts_code.split('.')[1]
        #print(name.lower())
        df_fund_daily = read_data(name.lower())
        df_fund_daily = df_fund_daily[['trade_date','close','open','high','low','vol']]

        if len(df_fund_daily) < 200:
            continue
        print(i)

        trade_data_start = df_fund_daily.iloc[0].trade_date
        trade_data_end = df_fund_daily.iloc[-1].trade_date
        #start_date = [int(trade_data_start[0:4]), int(trade_data_start[4:6]), int(trade_data_start[6:8])]
        #end_date = [int(trade_data_end[0:4]), int(trade_data_end[4:6]), int(trade_data_end[6:8])]
        start_date = [2022, 4, 27]
        end_date = [2022,6,15]

        #print('Name : %s' % df_fund_basic.name[i])
        #print(start_date, end_date)

        data = feeds_tushare(df_fund_daily, start_date, end_date)

        cerebro.adddata(data)  # 将数据传入回测系统
        cerebro.addstrategy(kitty_strategy2)  # 将数据传入回测系统
        #cerebro.addstrategy(boll_strategy)  # 将数据传入回测系统
        cerebro.broker.setcash(10000000000.0)
        cerebro.broker.setcommission(commission=0.0003)
        #print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        try:
            cerebro.run()
        except:
            pass
        #print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        #cerebro.plot()