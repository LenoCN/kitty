import pandas as pd

def inc_dist(o_list):

    da = pd.DataFrame(o_list,columns=['ts_code', 'trade_date', 'increase', 'decrease'])
    #print(da)
    len_all = len(da)
    if len_all == 0:
        return 0,0,0,0,0,0,0,0
    len_ic_1 = round(len(da[da['increase']>1.0])  /len_all, 3)
    len_ic_2 = round(len(da[da['increase']>1.005])/len_all, 3)
    len_ic_3 = round(len(da[da['increase']>1.01]) /len_all, 3)
    len_ic_4 = round(len(da[da['increase']>1.02]) /len_all, 3)
    len_ic_5 = round(len(da[da['increase']>1.03]) /len_all, 3)
    len_ic_6 = round(len(da[da['increase']>1.04]) /len_all, 3)
    len_ic_7 = round(len(da[da['increase']>1.05]) /len_all, 3)

    len_dc_6 = round(len(da[da['decrease']>0.9])  /len_all, 3)
    len_dc_7 = round(len(da[da['decrease']>0.95]) /len_all, 3)
    len_dc_8 = round(len(da[da['decrease']>0.98]) /len_all, 3)
    len_dc_9 = round(len(da[da['decrease']>0.99]) /len_all, 3)
    len_dc_a = round(len(da[da['decrease']>0.995])/len_all, 3)
    #print('len_all : ' , len_all, '>1 :', len_a/len_all, '>1.005 :' , len_b/len_all, '>1.01 :' , len_c/len_all, '>1.02 :' , len_d/len_all, '>1.05 :' , len_e/len_all)
    print('len_all : ' , len_all)
    print('>1.000 :' , len_ic_1)
    print('>1.005 :' , len_ic_2)
    print('>1.010 :' , len_ic_3)
    print('>1.020 :' , len_ic_4)
    print('>1.030 :' , len_ic_5)
    print('>1.040 :' , len_ic_6)
    print('>1.050 :' , len_ic_7)

    #print('>0.900 :' , len_dc_6)
    #print('>0.950 :' , len_dc_7)
    #print('>0.980 :' , len_dc_8)
    #print('>0.990 :' , len_dc_9)
    #print('>0.995 :' , len_dc_a)

    return [len_all, len_ic_1,len_ic_2,len_ic_3,len_ic_4,len_ic_5,len_ic_6,len_ic_7]