import numpy as np
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from symbols import symbols
import technical_indicators as ti
import argparse


def run():
    s_year = 2018
    s_month = 1
    s_day = 2
    e_year = 2018
    e_month = 6
    e_day = 30
    sym = symbols()
    sym_list = ['TSLA', 'AMD', 'SQ', 'DOCU']
    start = datetime.datetime(s_year, s_month, s_day)
    end = datetime.datetime(e_year, e_month, e_day)

    TI = ti.technical_indicators()
    num_days = 3
    n = 3

    data = {}
    data_stoch_k = {}
    data_stoch_k_ma = {}
    data_stoch_d = {}
    for s in sym_list:
        data[s] = sym.getSymbolData(s, start, end)
        data_stoch_k[s] = TI.stochastic_oscillator_k(data[s])
        data_stoch_d[s] = TI.stochastic_oscillator_d(data[s], num_days)
        data_stoch_k_ma[s] = TI.moving_average(data_stoch_k[s], 'SO%k', n)
        data_stoch_k_ma[s]['MA_3'].plot(label=s+' stoch_k')
        data_stoch_d[s]['SO%d_'+str(num_days)].plot(label=s+' stoch_d', figsize=(10, 8))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    run()
