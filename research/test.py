# 非阻塞示例
import multiprocessing
import time
import pstats
import pyarrow.parquet as pp
import sys
import pandas as pd


def func(txt):
    print("txt: ", txt)
    time.sleep(4)
    print("end")

if __name__ == '__main__':

    #df= pp.read_table('df_rtest_param_analysis.parquet').to_pandas()
    df= pp.read_table('df_rtest_param_analysis20220700.parquet').to_pandas()
    df = df.reset_index(drop=True)

    df = df.sort_values(by='ic7', ascending=False)
    #df = df[df['len_all']>300]

    #df = df[df['ic1'] > 0.9]
    #df = df.reset_index(drop=True)
    with pd.option_context('display.max_rows', None): 
        print(df)
    sys.exit()

    g = df.groupby('a')


    #p = pstats.Stats('test_status')
    ##p = pstats.Stats('rtest_status')

    ##p.strip_dirs().sort_stats(-1).print_stats(10)
    #p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)
    ##p.sort_stats(pstats.SortKey.TIME).print_stats(20)