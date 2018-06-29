import pandas as pd
import numpy as numpy
import datetime
import pandas_datareader
import pandas_datareader.data as web

class symbols(object):
    def __init__(self, symbol='A'):
        self.symStr = symbol        
        self.signal = None

    def getSymbolData(self, sym, startDate, endDate):
        start = startDate
        end = endDate
        self.symStr = sym
        symData = web.DataReader(self.symStr, 'morningstar', start, end)
        return symData

    def calcSignals(self, df_sod, df_sok, period):
        sodStr = 'SO%d_'+str(period)
        sokStr = 'SO%k'

        self.signal = df_sok[sokStr].subtract(df_sod[sodStr])
        last = self.signal[0]
        days_since_last_flip = 0
        last_toggle = False if last < 0 else True

        for c in self.signal:
            toggle = False if c < 0 else True
            if last_toggle == toggle:
                days_since_last_flip += 1
            else:
                days_since_last_flip = 0
                last_toggle = toggle

        if self.signal[-1] < 0 and abs(df_sok[sokStr][-1]) < 0.50:
            self.printSig('sell', days_since_last_flip)
        elif self.signal[-1] > 0 and abs(df_sok[sokStr][-1]) > 0.50:
            self.printSig('buy', days_since_last_flip)
            # print("{0} {1} buy: {2} ".format(signal.index.get_level_values(0)[0], signal.index.get_level_values(1)[-1], signal[-1]))
        else:
            self.printSig('hold', days_since_last_flip)
            # print("{0} {1} hold: {2} ".format(signal.index.get_level_values(0)[0], signal.index.get_level_values(1)[-1], signal[-1]))

    def printSig(self, s, d):
        t = 'buy' if s == 'sell' else s
        print("{0} {1} {2}: days since last {3}: {4} {5}".format(self.signal.index.get_level_values(0)[0], \
                                                                self.signal.index.get_level_values(1)[-1], \
                                                                t, \
                                                                s, \
                                                                d, \
                                                                self.signal[-1]))