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

    def getSymbolData(self, sym, startDate, endDate, source):
        start = startDate
        end = endDate
        self.symStr = sym
 
        symData = web.DataReader(self.symStr, source, start, end)
        if source == 'robinhood':
            symData = symData[int(len(symData)/2):]

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

    def calcSignals(self, df_sod, df_sok, df_smi, df_sig, period, ti):
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

        # print(df_sod[sodStr][-1], df_sok[sokStr][-1], df_smi[-1], df_sig[-1])
        if (self.signal[-1] < 0 and self.smi[-1] < 0):  # and df_smi[-1] < 40 and df_sok[sokStr][-1] < 80):
            sigStr = RED+'sell'
            self.printSig(sigStr, days_since_last_flip, df_sod, ti, sigStr)
        elif (self.signal[-1] > 0 and self.smi[-1] > 0): # and df_smi[-1] > -40 and df_sok[sokStr][-1] > 20):
            sigStr = GREEN+'buy'
            self.printSig(sigStr, days_since_last_flip, df_sod, ti, sigStr)
        else:
            self.printSig(YELLOW+'hold', days_since_last_flip, df_sod, ti, sigStr)

    def printSig(self, s, d, df, ti, current_sig):
        if s == RED+'sell':
            t = GREEN+'buy'
        elif s == GREEN+'buy':
            t = RED+'sell'
        else:
            t =  current_sig
        
        if ti.source == 'morningstar':
            print("{0} {1} {2}\033[0m : days since last {3}: \033[0m {4} -- {5} / {6}".format(df['Close'][-1], \
                                                                self.signal.index.get_level_values(0)[0], \
                                                                s, \
                                                                t, \
                                                                d, \
                                                                self.signal.index.get_level_values(1)[-1].date(), \
                                                                self.signal.index.get_level_values(1)[0].date())) 
        elif ti.source == 'robinhood':
            print("{0} {1} {2}\033[0m : days since last {3}: \033[0m {4} -- {5} / {6}".format(df['close_price'][-1], \
                                                                self.signal.index.get_level_values(0)[len(self.signal)-1], \
                                                                s, \
                                                                t, \
                                                                d, \
                                                                self.signal.index.get_level_values(1)[-1].date(), \
                                                                self.signal.index.get_level_values(1)[0].date())) 