# Function to calculate the daily return of a stock
def daily_return(close):
    """
    Calculate the daily return of a stock.

    Parameters
    ----------
    close: pandas.Series
        Series containing the stock data.

    Returns
    -------
    pandas.Series
        Series containing the daily return of a stock.
    """
    # Calculate the daily return of a stock
    daly_ret = close.pct_change()
    # Return the daily return of a stock
    return daly_ret


# Function to calculate the cumulative return of a stock
def cumulative_return(daily_ret):
    """
    Calculate the cumulative return of a stock.

    Parameters
    ----------
    daily_ret: pandas.Series
        DataFrame containing the stock data.

    Returns
    -------
    pandas.Series
        Series containing the cumulative return of a stock.
    """
    # Calculate the cumulative return of a stock
    cum_returns = (1 + daily_ret).cumprod()
    # Return the cumulative return of a stock
    return cum_returns


# Function to calculate Bollinger Bands
def bollinger_bands(df, window=20):
    """
    Calculate the Bollinger Bands of a stock.

    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame containing the stock data.
    window: int
        Window size for the Bollinger Bands.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the Bollinger Bands of a stock.
    """
    # Calculate the rolling mean of the stock
    df['RollingMean'] = df['Close'].rolling(window=window).mean()
    # Calculate the rolling standard deviation of the stock
    rolling_std = df['Close'].rolling(window=window).std()
    # Calculate the upper band
    df['UpperBand'] = df['RollingMean'] + (2 * rolling_std)
    # Calculate the lower band
    df['LowerBand'] = df['RollingMean'] - (2 * rolling_std)
    # Return the upper and lower bands
    return df


def cal_ichimoku(data, tenkan_window=9, kijun_window=26, senkou_span_b_window=52):
    """
    Calculate the Ichimoku Kinko Hyo (Ichimoku) indicator.
    Parameters
    ----------
    data: pandas.DataFrame
    senkou_span_b_window: int
        Window size for the senkou span B.
    kijun_window: int
        Window size for the kijun line.
    tenkan_window: int
        Window size for the tenkan line.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the Ichimoku indicator of a stock.
    """
    # Conversion
    hi_val = data['High'].rolling(window=tenkan_window).max()
    low_val = data['Low'].rolling(window=tenkan_window).min()
    data['Conversion'] = (hi_val + low_val) / 2

    # Baseline
    hi_val2 = data['High'].rolling(window=kijun_window).max()
    low_val2 = data['Low'].rolling(window=kijun_window).min()
    data['Baseline'] = (hi_val2 + low_val2) / 2

    # Spans
    data['SpanA'] = ((data['Conversion'] + data['Baseline']) / 2).shift(26)
    hi_val3 = data['High'].rolling(window=senkou_span_b_window).max()
    low_val3 = data['Low'].rolling(window=senkou_span_b_window).min()
    data['SpanB'] = ((hi_val3 + low_val3) / 2).shift(kijun_window)
    data['Lagging'] = data['Close'].shift(-kijun_window)

    return data


if __name__ == '__main__':
    pass
