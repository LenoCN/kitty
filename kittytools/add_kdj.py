import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

def add_kdj(data_frame, n=9, m1=3, m2=3):
    low_list = data_frame['low'].rolling(window=n).min()
    high_list = data_frame['high'].rolling(window=n).max()

    rsv = (data_frame['close'] - low_list) / (high_list - low_list) * 100

    k = rsv.ewm(com=m1-1).mean()
    d = k.ewm(com=m2-1).mean()
    j = 3 * k - 2 * d

    data_frame['k'] = k
    data_frame['d'] = d
    data_frame['j'] = j
    
    # 添加金叉列
    data_frame['kdj_jc'] = (k.shift(1) < d.shift(1)) & (k > d)
    
    # 添加KDJ顶背离列
    data_frame['kdj_dbl'] = ((k.shift(2) < k.shift(1)) &
                           (k.shift(1) > k) &
                           (data_frame['close'].shift(2) < data_frame['close'].shift(1)) &
                           (data_frame['close'].shift(1) < data_frame['close']))


    return data_frame