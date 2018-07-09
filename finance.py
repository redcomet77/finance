import numpy as np
import pandas as pd
import time
import datetime
from datetime import date
import matplotlib.pyplot as plt
from symbols import symbols
import technical_indicators as ti
import argparse
import csv

class test_instance(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def open_list(self):
        self.parser.add_argument("f", help="file to parse or default: watchlist.csv", default="watchlist.csv")
        self.args = self.parser.parse_args()

        with open(self.args.f, newline='') as csvfile:
            cr = csv.reader(csvfile)
            l = [i[0] for i in cr]            
        return l

    def run(self):
        sym = symbols()
        sym_list = self.open_list()
        end = date.today()
        start = datetime.datetime(end.year, end.month-6, end.day)
        TI = ti.technical_indicators()
        num_days = 3
        period14 = 14
        period10 = 10
        data = {}
        data_stoch_k = {}
        data_stoch_k_ma = {}
        data_stoch_d = {}
        data_smi = {}

        sap500 = sym.save_sp500_tickers()
        eval_list = sap500
        show_g = False

        for s in eval_list:            
            data[s] = sym.getSymbolData(s, start, end)
            data_stoch_k[s] = TI.stochastic_oscillator_k(data[s], period14)
            data_stoch_d[s] = TI.stochastic_oscillator_d(data[s], num_days, period14)
            data_stoch_k_ma[s] = TI.moving_average(data_stoch_k[s], 'SO%k', num_days)
            data_smi[s] = TI.stoch_momemtum_idx(data[s], num_days, period10)
            sym.calcSignals(data_stoch_d[s], data_stoch_k_ma[s], data_smi[s]['smi'], data_smi[s]['smi_sig'], period14)
            
            if show_g: 
                f = plt.figure(eval_list.index(s))
                f.canvas.set_window_title(s)
                f.add_subplot(211)
                data_stoch_k_ma[s]['MA_'+str(num_days)].plot(title=s, label=s+' stoch_k')
                data_stoch_d[s]['SO%d_'+str(period14)].plot(label=s+' stoch_d', figsize=(10, 4))
                plt.legend()
                f.add_subplot(212)
                data_smi[s]['smi'].plot(label=s+' smi', figsize=(10, 4))
                data_smi[s]['smi_sig'].plot(label=s+' smi_sig', figsize=(10, 4))
                f.autofmt_xdate()
                plt.xlabel(data_stoch_d[s].index.get_level_values(0)[1])
                plt.legend()

        if show_g:
            plt.show()

if __name__ == '__main__':
    test = test_instance()
    test.run()