import numpy as np
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from symbols import symbols

s_year = 2018
s_month = 1
s_day = 2
e_year = 2018
e_month = 6
e_day = 30
sym = symbols()
start = datetime.datetime(s_year, s_month, s_day)
end = datetime.datetime(e_year, e_month, e_day)
tesla = sym.getSymbolData('TSLA', start, end)
tesla['Close'].plot(label='TSLA', figsize=(10, 4))
sq = sym.getSymbolData('SQ', start, end)
sq['Close'].plot(label='SQ')
plt.legend()
plt.show()
