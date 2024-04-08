from ctypes import LittleEndianStructure
from mailbox import linesep
import sys
sys.path.append("C:\\Users\\liuwe\\Desktop\\kitty")
from kittytools.mysql import read_data
import time
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = read_data('test1011')
    trade_date_l = []
    for k,v in enumerate(df.trade_date):
        if v not in trade_date_l:
            trade_date_l.append(v)
    x = []
    y1 = []
    y2 = []
    for trade_date in trade_date_l:
        df_tmp = df[df['trade_date'] == trade_date]
        #df_tmp = df_tmp[df_tmp['increase'] != 0]
        l_tmp = df_tmp['increase'].to_list()
        mean = np.mean(l_tmp)
        if mean == 0:
            mean = 1
        x.append(trade_date[-4:])
        y1.append(mean-1)
        y2.append(len(l_tmp))
        #result_a.append({'trade_date':trade_date,'average_increase':mean})
        #print(df_tmp['increase'])

    fig,ax1 = plt.subplots()
    ax1.set_xlabel('trade_date')
    ax1.set_ylabel('average_increase')
    ax1.plot(x, y1,color='tab:blue')
    ax1.tick_params(axis='y',labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('nums')
    ax2.plot(x, y2, color='tab:red')
    ax2.tick_params(axis='y',labelcolor='tab:red')

    fig.tight_layout()
    plt.show()

    #plt.plot(x,y1)
    #plt.xlabel('trade_date')
    #plt.ylabel('average_increase')
    #plt.plot(x,y2,color='red',linestyle='--')
    #plt.show()

    #print(trade_date_l)