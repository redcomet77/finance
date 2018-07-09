import pandas as pd
import numpy as numpy
import datetime
import pandas_datareader
import pandas_datareader.data as web
import bs4 as bs
import pickle
import requests

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

    def save_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)

        with open("sp500tickers.pickle","wb") as f:
            pickle.dump(tickers,f)

        return tickers

    def calcSignals(self, df_sod, df_sok, df_smi, df_sig, period):
        sodStr = 'SO%d_'+str(period)
        sokStr = 'SO%k'

        self.signal = df_sok[sokStr].subtract(df_sod[sodStr])
        self.smi = df_smi.subtract(df_sig)
        last = self.signal[0]
        last2 = self.smi[0]
        days_since_last_flip = 0
        last_toggle = False if last < 0 and last2 < 0 else True
        sigStr = RED+'sell' if last < 0 and last2 < 0 else GREEN+'buy'

        for c, d in zip(self.signal, self.smi) :
            toggle = False if c < 0 and d < 0 else True
            if last_toggle == toggle:
                days_since_last_flip += 1
            else:
                days_since_last_flip = 0
                last_toggle = toggle

        if (self.signal[-1] < 0 and self.smi[-1] < 0):
            sigStr = RED+'sell'
            self.printSig(sigStr, days_since_last_flip)
        elif (self.signal[-1] > 0 and self.smi[-1] > 0):
            sigStr = GREEN+'buy'
            self.printSig(sigStr, days_since_last_flip)
        else:
            self.printSig(sigStr, days_since_last_flip)

    def printSig(self, s, d):
        t = GREEN+'buy' if s == RED+'sell' else RED+'sell'
        print("{0} {1} {2} \033[0m : days since last {3}: \033[0m {4} \n {5} {6}".format(self.signal.index.get_level_values(0)[0], \
                                                                self.signal.index.get_level_values(1)[-1], \
                                                                s, \
                                                                t, \
                                                                d, self.smi[-1], self.signal[-1]))
