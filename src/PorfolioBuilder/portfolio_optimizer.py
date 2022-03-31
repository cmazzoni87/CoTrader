import os,sys
sys.path.insert(0, os.path.abspath('..'))
import pandas as pd
import numpy as np
from datetime import datetime
from variables import *
from utilities import prep_dir
import os

DATA_PATH = prep_dir("C:\\", "Co_Trader_Files")
SEC_DATA_PATH = prep_dir(DATA_PATH, "SecData")

def compile_fields_from_csv(security_list: list, field: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    sec_returns = dict()

    for sec in security_list:
        sec_info = pd.read_csv(os.path.join(SEC_DATA_PATH, "{}.csv".format(sec)))
        sec_info['Date'] = pd.to_datetime(sec_info['Date'])
        sec_info = sec_info[(sec_info['Date'] >= start_date) & (sec_info['Date'] <= end_date)]
        sec_returns[sec] = sec_info[field]#.tolist()
    return pd.DataFrame(sec_returns)


def get_port_shares(one_price, force_one, wts, prices):
    # Gets number of stocks to analyze
    num_stocks = len(wts)

    # Holds the number of shares for each
    shares = []

    # Holds Cost of shares for each
    cost_shares = []

    i = 0
    while i < num_stocks:
        # Get max amount to spend on stock
        max_price = one_price * wts[i]

        # Gets number of shares to buy and adds them to list
        num_shares = int(max_price / prices[i])
        # If the user wants to force buying one share do it
        if (force_one & (num_shares == 0)):
            num_shares = 1

        shares.append(num_shares)

        # Gets cost of those shares and appends to list
        cost = num_shares * prices[i]
        cost_shares.append(cost)
        i += 1

    return shares, cost_shares


def get_port_weighting(share_cost):
    # Holds weights for stocks
    stock_wts = []
    # All values summed
    tot_val = sum(share_cost)
    print("Total Investment :", tot_val)

    for x in share_cost:
        stock_wts.append(x / tot_val)
    return stock_wts


def get_port_val(prices):
    port_prices = prices
    # Convert from dataframe to Python list
    port_prices = port_prices.values.tolist()
    # Trick that converts a list of lists into a single list
    port_prices = sum(port_prices, [])
    return port_prices


if __name__ == '__main__':
    stonks = ['CALX', 'TSLA', 'RGEN', 'LLY', 'AMD', 'NFLX', 'COST', 'BJ', 'WING', 'G', 'CBRE']
    stonks = [os.path.splitext(x)[-2] for x in os.listdir(SEC_DATA_PATH) if
                      (os.path.splitext(x)[-1] == '.csv' and os.path.splitext(x)[-2].upper() in stonks)]

    num_stocks = len(stonks)
    S_DATE = '2019-02-01'
    E_DATE = '2022-12-06'
    START_DATE = pd.to_datetime(S_DATE)
    END_DATE = pd.to_datetime(E_DATE)
    risk_free_rate = 0.0125  # Approximate 10 year bond rate
    trade_period = 252  # Average trading days per year

    prices = compile_fields_from_csv(stonks, 'Close', START_DATE, END_DATE)
    # cum_returns = compile_fields_from_csv(stonks, 'CumulativeReturn', START_DATE, END_DATE)

    returns = np.log(prices / prices.shift(1))
    mean_ret = returns.mean() * trade_period  # 252 average trading days per year
    returns_corr = returns.corr()
    weights = np.random.random(num_stocks)
    weights /= np.sum(weights)
    print('Weights :', weights)
    print('Total Weight :', np.sum(weights))
    # Provide return of portfolio using random weights over the whole dataset
    rand_w_returns = np.sum(weights * returns.mean()) * trade_period

    #Analyzing Returns & Risks of 10000 Combinations
    p_ret = []  # Returns list
    p_vol = []  # Volatility list
    p_SR = []  # Sharpe Ratio list
    p_wt = []  # Stock weights list

    for x in range(10000):
        # Generate random weights
        p_weights = np.random.random(num_stocks)
        p_weights /= np.sum(p_weights)

        # Add return using those weights to list
        ret_1 = np.sum(p_weights * returns.mean()) * trade_period
        p_ret.append(ret_1)

        # Add volatility or standard deviation to list
        vol_1 = np.sqrt(np.dot(p_weights.T, np.dot(returns.cov() * trade_period, p_weights)))
        p_vol.append(vol_1)

        # Get Sharpe ratio
        # This is dividing by 0
        SR_1 = (((ret_1 - risk_free_rate) / vol_1) if vol_1 != 0 else 0)
        p_SR.append(SR_1)

        # Store the weights for each portfolio
        p_wt.append(p_weights)

    # Convert to Numpy arrays
    p_ret = np.array(p_ret)
    p_vol = np.array(p_vol)
    p_SR = np.array(p_SR)
    p_wt = np.array(p_wt)

    # Return the index of the largest Sharpe Ratio
    SR_idx = np.argmax(p_SR)

    # Find the ideal portfolio weighting at that index
    i = 0
    while i < num_stocks:
        print("Stock : %s : %2.2f" % (stonks[i], (p_wt[SR_idx][i] * 100)))
        i += 1

    # Find volatility of that portfolio
    print("\nVolatility :", p_vol[SR_idx])

    # Find return of that portfolio
    print("Return :", p_ret[SR_idx])
    port_list = stonks

    port_wts = [7, 8, 15, 14, 3, 3, 17, 6, 11, 14, 1]

    # Get all stock prices on the starting date
    port_df_start = prices
    # Convert from dataframe to Python list
    port_prices = port_df_start.values.tolist()

    # Trick that converts a list of lists into a single list
    port_prices = sum(port_prices, [])

    tot_shares, share_cost = get_port_shares(105.64, True, port_wts, port_prices)
    print("Shares :", tot_shares)
    print("Share Cost :", share_cost)

    # Get list of weights for stocks
    stock_wts = get_port_weighting(share_cost)
    print("Stock Weights :", stock_wts)

    # Get value at end of year
    # get_port_val(prices)
