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
