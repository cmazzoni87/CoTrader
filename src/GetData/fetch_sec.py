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
from utilities import prep_dir
import traceback

DATA_PATH = prep_dir("C:\\", "Co_Trader_Files")
SEC_DATA_PATH = prep_dir(DATA_PATH, "SecData")
MARKETS_DATA_PATH = prep_dir(DATA_PATH, "Markets")
INDUSTRY_DATA_PATH = prep_dir(MARKETS_DATA_PATH, "Industry")
SEC_IGNORE_LIST_PATH = os.path.join(DATA_PATH, "sec_ignore_list.csv")
SEC_IGNORE_LIST = pd.read_csv(SEC_IGNORE_LIST_PATH)

def save_to_csv_from_yahoo(tick: str, cherry_pick: bool = True) -> any:
    # Reads data into a dataframe
    try:
        stock = yf.Ticker(tick)
        df = stock.history(period='5y')
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None
    if df.shape[0] < 50:
    #if df.shape[0] < 256:
        print(df.shape[0])
        return None
    df['DailyReturn'] = daily_return(df['Close'])
    df['CumulativeReturn'] = cumulative_return(df['DailyReturn'])
    df = bollinger_bands(df)
    df = cal_ichimoku(df)
    # Saves data to csv
    out_path = os.path.join(SEC_DATA_PATH, "{}.csv".format(tick))
    df.to_csv(out_path)
    if cherry_pick:
        return df['CumulativeReturn'].iloc[-1]
    else:
        return None


def save_sector_performance(sectors_returns: dict) -> None:
    for key, value in sectors_returns.items():
        df = pd.DataFrame(sectors_returns[key], columns=['Ticker', 'CumulativeReturn'])
        df = df.sort_values(by=['CumulativeReturn'], ascending=False)
        out_path = os.path.join(INDUSTRY_DATA_PATH, "{}.csv".format(key))
        df.to_csv(out_path)

def init_get_stock_data(ignore_existing=True) -> None:
    nasdaq_tickers = get_ticker_list()
    #Ignore securities we have already seen and unsuccessfully tried to download
    nasdaq_tickers = [[x,y] for x,y in nasdaq_tickers if x not in SEC_IGNORE_LIST['Ticker'].values]

    #Ignore securities we already downloaded at some point, to speed up this process
    if not ignore_existing:
        existing_sec_list = [os.path.splitext(x)[-2] for x in os.listdir(SEC_DATA_PATH) if os.path.splitext(x)[-1] == '.csv']
        nasdaq_tickers = [[x,y] for x,y in nasdaq_tickers if x not in existing_sec_list]

    sector_cum_returns = defaultdict(list)
    for ticker, sector in nasdaq_tickers:
        # remove non alphanumeric characters using regex
        try:
            sector = re.sub(r'[^a-zA-Z0-9]', '', sector)
        except Exception as e:
            SEC_IGNORE_LIST.loc[len(SEC_IGNORE_LIST)] = [ticker]
            SEC_IGNORE_LIST.to_csv(SEC_IGNORE_LIST_PATH, index=False)
            print(sector)
            print(e)
            continue
        result = save_to_csv_from_yahoo(ticker)
        if result is not None:
            sector_cum_returns[sector].append([ticker, result])
        else:
            print(ticker + ' failed')
            SEC_IGNORE_LIST.loc[len(SEC_IGNORE_LIST)] = [ticker]
            SEC_IGNORE_LIST.to_csv(SEC_IGNORE_LIST_PATH, index=False)
    save_sector_performance(sector_cum_returns)

if __name__ == "__main__":
    init_get_stock_data(ignore_existing=False)
