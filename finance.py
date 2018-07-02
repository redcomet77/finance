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
    sym_list = ('GBTC', 'TSLA', 'AMD', 'SQ', 'DOCU', \
                'IQ', 'NVDA', 'MU', 'ROKU', 'CMG', \
                'NFLX', 'INTC', 'CRM', 'WDAY', 'TWTR', \
                'AMZN', )
    start = datetime.datetime(s_year, s_month, s_day)
    end = datetime.datetime(e_year, e_month, e_day)

    TI = ti.technical_indicators()
    num_days = 3
    period14 = 14
    period10 = 10
    data = {}
    data_stoch_k = {}
    data_stoch_k_ma = {}
    data_stoch_d = {}
    data_smi = {}

    for s in sym_list:
        f = plt.figure(sym_list.index(s))
        f.canvas.set_window_title(s)
        data[s] = sym.getSymbolData(s, start, end)
        data_stoch_k[s] = TI.stochastic_oscillator_k(data[s], period14)
        data_stoch_d[s] = TI.stochastic_oscillator_d(data[s], num_days, period14)
        data_stoch_k_ma[s] = TI.moving_average(data_stoch_k[s], 'SO%k', num_days)
        data_smi[s] = TI.stoch_momemtum_idx(data[s], num_days, period10)

        sym.calcSignals(data_stoch_d[s], data_stoch_k_ma[s], data_smi[s]['som2'], data_smi[s]['dsmi_2'], period14)

        f.add_subplot(211)
        data_stoch_k_ma[s]['MA_'+str(num_days)].plot(title=s, label=s+' stoch_k')
        data_stoch_d[s]['SO%d_'+str(period14)].plot(label=s+' stoch_d', figsize=(10, 4))
        # plt.xlabel(data_stoch_d[s].index.get_level_values(0)[1])
        plt.legend()
        f.add_subplot(212)
        data_smi[s]['som2'].plot(label=s+' k', figsize=(10, 4))
        data_smi[s]['dsmi_2'].plot(label=s+' dsmi', figsize=(10, 4))
        f.autofmt_xdate()

        # plt.xlabel(data_stoch_d[s].index.get_level_values(0)[1])
        plt.legend()

    plt.show()


if __name__ == '__main__':
    run()
