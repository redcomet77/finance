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
    sym_list = ('gbtc', 'TSLA', 'AMD', 'SQ', 'DOCU', 'IQ', 'NVDA', 'MU', 'NFLX', 'INTC', 'CRM', 'WDAY', 'TWTR')
    start = datetime.datetime(s_year, s_month, s_day)
    end = datetime.datetime(e_year, e_month, e_day)

    TI = ti.technical_indicators()
    num_days = 3
    period = 14
    fig, axes = plt.subplots(nrows=len(sym_list))

    data = {}
    data_stoch_k = {}
    data_stoch_k_ma = {}
    data_stoch_d = {}
    for s in sym_list:
        data[s] = sym.getSymbolData(s, start, end)
        data_stoch_k[s] = TI.stochastic_oscillator_k(data[s], period)
        data_stoch_d[s] = TI.stochastic_oscillator_d(data[s], num_days, period)
        data_stoch_k_ma[s] = TI.moving_average(data_stoch_k[s], 'SO%k', num_days)

        axes[sym_list.index(s)].set_xlabel(data_stoch_k_ma[s].index.get_level_values(1))
        data_stoch_k_ma[s]['MA_'+str(num_days)].plot(label=s+' stoch_k', ax=axes[sym_list.index(s)], title=s)
        data_stoch_d[s]['SO%d_'+str(period)].plot(label=s+' stoch_d', ax=axes[sym_list.index(s)], figsize=(15, 10))
        sym.calcSignals(data_stoch_d[s], data_stoch_k_ma[s], period)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    run()
