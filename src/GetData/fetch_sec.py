import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from collections import defaultdict
import pandas as pd
import re
import yfinance as yf
from DoTechnicals.core_fundamentals import *
from fetch_index import *
from variables import *


def save_to_csv_from_yahoo(tick: str, cherry_pick: bool = True) -> any:
    # Reads data into a dataframe
    try:
        stock = yf.Ticker(tick)
        df = stock.history(period='max')
    except Exception as e:
        print(e)
        return None
    df['DailyReturn'] = daily_return(df['Close'])
    df['CumulativeReturn'] = cumulative_return(df['DailyReturn'])
    df = bollinger_bands(df)
    df = cal_ichimoku(df)
    # Saves data to csv
    df.to_csv(DATA_PATH + '\\SecData\\' + tick + '.csv')
    if cherry_pick:
        return df['CumulativeReturn'].iloc[-1]
    else:
        return None


def save_sector_performance(sectors_returns: dict) -> None:
    for key, value in sectors_returns.items():
        df = pd.DataFrame(sectors_returns[key], columns=['Ticker', 'CumulativeReturn'])
        df = df.sort_values(by=['CumulativeReturn'], ascending=False)
        df.to_csv(DATA_PATH + '\\Markets\\Industry\\' + key + '.csv')


def init_get_stock_data() -> None:
    nasdaq_tickers = get_ticker_list()
    sector_cum_returns = defaultdict(list)
    for ticker, sector in nasdaq_tickers:
        # remove non alphanumeric characters using regex
        sector = re.sub(r'[^a-zA-Z0-9]', '', sector)
        sector_cum_returns[sector].append([ticker, save_to_csv_from_yahoo(ticker)])
    save_sector_performance(sector_cum_returns)

init_get_stock_data()