def add_macd(data_frame, short=12, long=26, m=9):
    ewma_short = data_frame['close'].ewm(span=short).mean()
    ewma_long = data_frame['close'].ewm(span=long).mean()

    dif = ewma_short - ewma_long
    dea = dif.ewm(span=m).mean()
    macd = 2 * (dif - dea)

    data_frame['dif'] = dif
    data_frame['dea'] = dea
    data_frame['macd'] = macd

    # 添加死叉列
    data_frame['macd_sc'] = (dif.shift(1) > dea.shift(1)) & (dif < dea)

    return data_frame