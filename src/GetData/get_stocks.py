import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from os.path import exists
from variables import *
import pandas as pd
import time
import requests
import json
import yfinance as yf
from DoTechnicals.core_fundamentals import *
from collections import defaultdict


def get_sec_data():
    url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    req = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
    a_json = json.loads(req.text)
    securities = pd.DataFrame(a_json['data']['rows'])
    # Uppercase all column names
    securities.columns = map(str.title, securities.columns)
    securities = securities[securities['Sector'] != '']
    return securities


def get_ticker_list(days_to_stale: int = 7):
    nasdaq_path = DATA_PATH + '\\Markets\\NASDAQ.csv'
    if exists(nasdaq_path):
        creation_time = os.path.getctime(nasdaq_path)
        current_time = time.time()
        if (current_time - creation_time) // (24 * 3600) >= days_to_stale:
            nasdaq = get_sec_data()
            nasdaq.to_csv(nasdaq_path)
        else:
            nasdaq = pd.read_csv(nasdaq_path)
    else:
        nasdaq = get_sec_data()
        nasdaq.to_csv(nasdaq_path)
    tickers = nasdaq[['Symbol', 'Industry']].values.tolist()
    return tickers


def save_to_csv_from_yahoo(tick: str, cherry_pick: bool = True):
    # Reads data into a dataframe
    try:
        stock = yf.Ticker(tick)
        df = stock.history(period='max')
    except Exception as e:
        print(e)
        return
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


def save_sector_performance(sectors_returns: dict):
    for key, value in sectors_returns.items():
        df = pd.DataFrame(sectors_returns[key], columns=['Ticker', 'CumulativeReturn'])
        df = df.sort_values(by=['CumulativeReturn'], ascending=False)
        df.to_csv(DATA_PATH + '\\Markets\\Industry\\' + key + '.csv')


def init_get_stock_data():
    nasdaq_tickers = get_ticker_list()
    sector_cum_returns = defaultdict(list)
    for ticker, sector in nasdaq_tickers:
        sector_cum_returns[sector].append([ticker, save_to_csv_from_yahoo(ticker)])
    save_sector_performance(sector_cum_returns)

