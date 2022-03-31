import time
import requests
import json
from os.path import exists, join
import pandas as pd
from variables import *
from utilities import prep_dir

DATA_PATH = prep_dir("C:\\", "Co_Trader_Files")
MARKETS_DATA_PATH = prep_dir(DATA_PATH, "Markets")

def get_sec_index() -> pd.DataFrame:
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

def get_ticker_list(days_to_stale: int = 7) -> list:
    nasdaq_path = join(DATA_PATH,"NASDAQ.csv")
    print(nasdaq_path)
    if exists(nasdaq_path):
        creation_time = os.path.getctime(nasdaq_path)
        current_time = time.time()
        if (current_time - creation_time) // (24 * 3600) >= days_to_stale:
            nasdaq = get_sec_index()
            nasdaq.to_csv(nasdaq_path)
        else:
            nasdaq = pd.read_csv(nasdaq_path)
    else:
        nasdaq = get_sec_index()
        nasdaq.to_csv(nasdaq_path)
    # ##
    # nasdaq = nasdaq[nasdaq['Symbol'].isin(['CALX', 'TSLA', 'RGEN', 'LLY', 'AMD', 'NFLX', 'COST', 'BJ', 'WING', 'G',
    #                                        'CBRE'])]
    # ##
    tickers = nasdaq[['Symbol', 'Industry']].values.tolist()
    return tickers
