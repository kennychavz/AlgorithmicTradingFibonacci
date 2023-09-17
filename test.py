import pandas as pd
from commons import filterBy
# retrieve backtesting data and filter by stocks
# df = pd.read_json("data/5m_ml.json")
# stocks = ['AAPL', 'ADBE', 'AMZN', 'BAC', 'CSCO', 'DAL', 'DIS', 'GE', 'GOOGL', 'IBM', 'INTC'
#     'JNJ', 'JPM', 'KO', 'META', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'PFE', 'PG'
#     'PYPL', 'QCOM', 'SBUX', 'SPLK', 'T', 'TSLA', 'WMT']
# filtered_df = filterBy(df, "symbol", stocks)
# # profits > 0.5%
# filtered_df = filtered_df[abs(filtered_df.takeProfit1/filtered_df.entryPrice - 1) >= 0.005]
# # filtering by date
# filtered_df['date'] = pd.to_datetime(filtered_df['dateD'])
# filtered_df = filtered_df.sort_values(by='date')
# #filtered_df.set_index('date', inplace=True)

# filtered_df.to_json("data/backtest.json")

#print(pd.read_json("data/backtest.json"))

import pandas as pd

from alpha import get_alpha
from commons import *
from quant import *
from plotting import *
from metrics import metrics

# retrieve backtesting data and filter by stocks
filtered_df = pd.read_json("data/backtest.json")
filtered_df.set_index('date', inplace=True)
filtered_df['profit'] *= 0.05

metrics_df = metrics(filtered_df)
metrics_df = metrics_df.round(2)

print(metrics_df)
