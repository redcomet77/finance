import pandas as pd
import numpy as numpy
import datetime
import pandas_datareader
import pandas_datareader.data as web

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

class symbols(object):
    def __init__(self, symbol='A'):
        self.symStr = symbol        
        self.signal = None
        self.smi = None

    def getSymbolData(self, sym, startDate, endDate):
        start = startDate
        end = endDate
        self.symStr = sym
        symData = web.DataReader(self.symStr, 'morningstar', start, end)
        return symData

    def calcSignals(self, df_sod, df_sok, df_smi, df_sig, period):
        sodStr = 'SO%d_'+str(period)
        sokStr = 'SO%k'

        self.signal = df_sok[sokStr].subtract(df_sod[sodStr])
        self.smi = df_smi.subtract(df_sig)
        last = self.signal[0]
        days_since_last_flip = 0
        last_toggle = False if last < 0 else True

        for c, d in zip(self.signal, self.smi) :
            toggle = False if c < 0 and d < 0 else True
            if last_toggle == toggle:
                days_since_last_flip += 1
            else:
                days_since_last_flip = 0
                last_toggle = toggle

        if (self.signal[-1] < 0 and self.smi[-1] < 0):
            self.printSig(RED+'sell', days_since_last_flip)
        elif (self.signal[-1] > 0 and self.smi[-1] > 0):
            self.printSig(GREEN+'buy', days_since_last_flip)
        else:
            self.printSig(YELLOW+'hold', days_since_last_flip)

    def printSig(self, s, d):
        t = GREEN+'buy' if s == RED+'sell' else YELLOW+'hold'
        print("{0} {1} {2} \033[0m : days since last {3}: \033[0m {4}".format(self.signal.index.get_level_values(0)[0], \
                                                                self.signal.index.get_level_values(1)[-1], \
                                                                s, \
                                                                t, \
                                                                d))
