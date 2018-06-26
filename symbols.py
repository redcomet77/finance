import pandas as pd
import numpy as numpy
import datetime
import pandas_datareader
import pandas_datareader.data as web

class symbols:
    def __init__(self, symbol='A'):
        self.symStr = symbol

    def getSymbolData(self, sym, startDate, endDate):
        start = startDate
        end = endDate
        self.symStr = sym
        symData = web.DataReader(self.symStr, 'morningstar', start, end)
        return symData

    def calcSignals(self, df_sod, df_sok, period):
        sodStr = 'SO%d_'+str(period)
        sokStr = 'SO%k'

        signal = df_sok[sokStr].subtract(df_sod[sodStr])
        last = signal.tail()

        if last[-1] < 0 and abs(df_sok[sokStr][-1]) < 0.50:
            print("{0} {1} sell: {2} ".format(signal.index.get_level_values(0)[0], signal.index.get_level_values(1)[-1], signal[-1]))
        elif last[-1] > 0 and abs(df_sok[sokStr][-1]) > 0.50:
            print("{0} {1} buy: {2} ".format(signal.index.get_level_values(0)[0], signal.index.get_level_values(1)[-1], signal[-1]))
        else:
            print("{0} {1} hold: {2} ".format(signal.index.get_level_values(0)[0], signal.index.get_level_values(1)[-1], signal[-1]))