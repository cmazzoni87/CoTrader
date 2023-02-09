# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask,render_template,request
import flask
import json
import numpy as np
import requests
from flask_cors import CORS
from datetime import datetime
from datetime import date
from datetime import timedelta
from src.PorfolioBuilder import portfolio_optimizer
import pandas as pd
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/porfolios',methods = ['GET'])
def profolios():
#    with open("porfolios.json", "r") as f:
#        data = json.load(f)
    stock1 = {"name" : "porfolio1","stonks": ['CALX', 'TSLA', 'RGEN', 'LLY', 'AMD', 'NFLX', 'COST', 'WWE', 'WING', 'G', 'CBRE']}
    #stock2 = {"name" : "porfolio2","stonks": ['CALX', 'TSLA', 'RGEN']}
    #stock3 = {"name" : "porfolio1","stonks": {}}

    data=[];
    data.append(stock1);
    #data.append(stock2);
    return flask.jsonify(data)

@app.route('/statistics',methods = ['GET'])
def statistics():
    list = request.args.getlist('array[]');
    stonks = np.array(list);

    #END_DATE = date.today();
    #S_DATE = today - timedelta(days = 3)
    num_stocks = len(stonks)
    S_DATE = '2022-12-05'
    E_DATE = '2022-12-06'
    START_DATE = pd.to_datetime(S_DATE)
    END_DATE = pd.to_datetime(E_DATE)
    risk_free_rate = 0.0125  # Approximate 10 year bond rate
    trade_period = 252  # Average trading days per year
    # will return the prices of the stocks at the start date
    open = portfolio_optimizer.compile_fields_from_csv(stonks, 'Open', START_DATE, END_DATE)
    high = portfolio_optimizer.compile_fields_from_csv(stonks, 'High', START_DATE, END_DATE)
    low = portfolio_optimizer.compile_fields_from_csv(stonks, 'Low', START_DATE, END_DATE)
    prices = portfolio_optimizer.compile_fields_from_csv(stonks, 'Close', START_DATE, END_DATE)
    volume = portfolio_optimizer.compile_fields_from_csv(stonks, 'Volume', START_DATE, END_DATE)
    dividends = portfolio_optimizer.compile_fields_from_csv(stonks, 'Dividends', START_DATE, END_DATE)

    port_df_start = prices
    # Convert from dataframe to Python list
    port_prices = port_df_start.values.tolist()

    # Trick that converts a list of lists into a single list
    port_prices = sum(port_prices, [])

    returns = np.log(prices / prices.shift(1))
    mean_ret = returns.mean() * trade_period  # 252 average trading days per year
    returns_corr = returns.corr()
    weights = np.random.random(num_stocks)
    weights /= np.sum(weights)

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
    #print("\nVolatility :", p_vol[SR_idx])

    # Find return of that portfolio
    #print("Return :", p_ret[SR_idx])


    port_list = stonks

    port_wts = [7, 8, 15, 14, 3, 3, 17, 6, 11, 14, 2]

    # Get all stock prices on the starting date
    port_df_start = prices
    # Convert from dataframe to Python list
    port_prices = port_df_start.values.tolist()
    port_open=open.values.tolist()
    port_high=high.values.tolist()
    port_low=low.values.tolist()
    port_volume=volume.values.tolist()
    port_dividends=dividends.values.tolist()

    # Trick that converts a list of lists into a single list
    port_open = sum(port_open, [])
    port_high = sum(port_high, [])
    port_low = sum(port_low, [])
    port_prices = sum(port_prices, [])
    port_volume = sum(port_volume, [])
    port_dividends = sum(port_dividends, [])
    tot_shares, share_cost = portfolio_optimizer.get_port_shares(105.64, True, port_wts, port_prices)

    total_cost = 0;
    for cost in share_cost:
        total_cost+=cost

    # Get list of weights for stocks
    stock_wts = portfolio_optimizer.get_port_weighting(share_cost)

    # Get value at end of year
    # get_port_val(prices)

    data = {"portfolio_Data":{},"stock_data":[]};

    if pd.isna(p_vol[SR_idx]):
        data["portfolio_Data"]["voltality"]= 0;
    else:
        data["portfolio_Data"]["voltality"]=p_vol[SR_idx];

    data["portfolio_Data"]["return"]=p_ret[SR_idx];
    data["portfolio_Data"]["total_cost"]=total_cost;
    # print(total_cost);
    i=0;
    for stonk in stonks:
        data["stock_data"].append({"symbol":stonk,"open":port_open[i],"high":port_high[i],"low":port_low[i],"close":port_prices[i],
"volume":port_volume[i],"dividends":port_dividends[i],"total_shares":tot_shares[i],"share_cost":share_cost[i],"stock_wts":stock_wts[i]});
        i+=1;
    # news section

    return flask.jsonify(data)

@app.route('/news',methods=['GET'])
def news():
    list = request.args.getlist('array[]');
    stocks=",".join(list);
    url = ( 'https://api.marketaux.com/v1/news/all?symbols='+stocks+'&filter_entities=true&language=en&api_token=VsauOeyFVu6oDtf2T1gaB4c4z1qbC6PsCJctlEqc');
    response = requests.get(url);
    j=json.loads(response.text)
    return flask.jsonify(j)

@app.route('/chart',methods=['GET'])
def chart():
    # start = requests.args.get('start');
    # end = requests.args.get('end');
    S_DATE = '2021-12-05'
    E_DATE = '2022-12-06'
    START_DATE = pd.to_datetime(S_DATE)
    END_DATE = pd.to_datetime(E_DATE)
    stocks = request.args.getlist('array[]');
    print(stocks)
    dict = {"portfolio_chart_data": {"dates":[],"data":[]},"stock_chart_data": {}}

    dateLength = 0
    for stock in stocks:
        temp=[stock]
        prices = portfolio_optimizer.compile_fields_from_csv(temp, 'Close', START_DATE, END_DATE)
        prices = prices.values.tolist()
        prices = sum(prices,[]);
        dates = portfolio_optimizer.compile_fields_from_csv(temp, 'Date', START_DATE, END_DATE)
        dates = dates.values.tolist()
        dates = sum(dates,[]);
        dict["stock_chart_data"][stock] = {}
        dict["stock_chart_data"][stock]["prices"] = prices
        dict["stock_chart_data"][stock]["dates"] = {};
        dict["stock_chart_data"][stock]["dates"]= dates
        dateLength=len(dates);
        dict["portfolio_chart_data"]["dates"]=dates;

    arr = np.zeros(dateLength);
    for stock in stocks:
        temp = np.array(dict["stock_chart_data"][stock]["prices"])
        arr=np.add(arr,temp);
    dict["portfolio_chart_data"]["data"] = arr.tolist();
    return flask.jsonify(dict)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
