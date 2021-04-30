# core imports
from datetime import datetime
import numpy as np
import pandas as pd
from time import sleep


# AplhaVantageAPI
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

tickers = ['AAPL','ACN','ADBE','ADI','ADP','ADSK','AKAM','AMAT','AMD','ANET','ANSS','APH','AVGO','BR','CDNS','CDW','CRM','CSCO','CTSH','CTXS','DXC','ENPH','FFIV','FIS','FISV','FLIR','FLT','FTNT','GLW','GPN','HPE','HPQ','IBM','INTC','INTU','IPGP','IT','JKHY','JNPR','KEYS','KLAC','LRCX','MA','MCHP','MPWR','MSFT','MSI','MU','MXIM','NLOK','NOW','NTAP','NVDA','NXPI','ORCL','PAYC','PAYX','PYPL','QCOM','QRVO','SNPS','STX','SWKS','TEL','TER','TRMB','TXN','TYL','V','VRSN','WDC','WU','XLNX','ZBRA']


def API(ticker):
    """[Pulls API data for stock market data and concatenates
        price/vol tables with technical indicators.]

    Args:
        ticker ([list]): [List of tickers]

    Returns:
        [DataFrame]: [stock specific table with all price/vol.
        and technical indicator data]
    """
    API_key = 'CSMN0LYTQ5UYMVUT'
    API_URL = "https://www.alphavantage.co/query"
    
    # call for price and volume
    ts = TimeSeries(key=API_key, output_format='pandas')
    price = ts.get_daily_adjusted(ticker, outputsize='full')[0]
    
    # Calls for technical indicators
    ti = TechIndicators(key=API_key, output_format='pandas')
    
    macd, meta_data = ti.get_macd(symbol=ticker,interval='daily')
    bbands, meta_data = ti.get_bbands(symbol=ticker,interval='daily')
    rsi,meta_data = ti.get_rsi(symbol=ticker,interval='daily',time_period=15)
    sma5, meta_data = ti.get_sma(symbol=ticker,time_period=5)
    sma15, meta_data = ti.get_sma(symbol=ticker,time_period=15)
    roc, meta_data = ti.get_roc(symbol=ticker,series_type='high',interval='daily')
    cci, meta_data = ti.get_cci(symbol=ticker,time_period=60,interval='daily')
    dx, meta_data = ti.get_dx(symbol=ticker,time_period=60,interval='daily')
    
    # Concatenation
    data = pd.concat([price, macd, bbands, rsi, sma5, sma15, roc, cci, dx], axis=1)
    data = data.dropna()
    # data['ticker'] = ticker
    return data
    
    
    
def crossover(data):
    """[Adds column for MACD crossover indicator.]

    Args:
        data ([DataFrame]): [Ticker specific table of stock
        market data.]

    Returns:
        [DataFrame]: [DataFrame with additional column.]
    """
    data['crossover'] = data['MACD'] > data['MACD_Signal']
    return data
def alpha(data):
    """[Sets start date for each dataframe.]

    Args:
        data ([DataFrame]): [Ticker specific table of stock
        market data.]

    Returns:
        [DataFrame]: [Trimmed DataFrame]
    """
    return data[data.index>=datetime(2020, 1, 1)]
def omega(data, period):
    """[Sets end date for each DataFrame, determined by period
        passed through. ]

    Args:
        data ([DataFrame]): [Ticker specific table of stock
        market data.]
        period ([string]): [Indicates how far back the DataFrame
        ends.]

    Returns:
        [DataFrame]: [Date bound data]
    """
    #TODO add 'today' and 'today - nDays'
    if period == '3day':
        end = datetime(2021, 4, 24)
    if period == '7day':
        end = datetime(2021, 4, 20)
    elif period == '30day':
        end = datetime(2021, 3, 28)
    elif period == '90day':
        end = datetime(2021, 4, 28)
    else: end = datetime(2021, 3, 28)
    return data[data.index<=end]


def dropcols(data):
    """[Drops unnecessary columns]

    Args:
        data ([DataFrame]): [Ticker specific table of stock
        market data.]

    Returns:
        [DataFrame]: [DataFrame with reduced features]
    """
    data = data.drop(columns=['4. close', '7. dividend amount', '8. split coefficient'])
    return data
def feature_names(data):
    """[Renames columns for clairity and training environment
        requirements: Whatever close price used bust be labelled 'Close'.]

    Args:
        data ([DataFrame]): [Ticker specific table of stock
        market data.]

    Returns:
        [DataFrame]: [DataFrame with renamed columns]
    """
    data = data.rename(columns={'1. open':'open', '2. high':'high', '3. low':'low', '5. adjusted close':'Close', '6. volume':'vol'})
    return data


def preprocess_data(tickers, period, save=True):
    """[Combines in all preprocessing functions with some additional cleanup,
        saves data to csv, and ensures API rate limit is not exceded.]

    Args:
        tickers ([List or String]): [List of tickers, or single ticker.]
        period ([string]): [Indicates date cutoff]
        save (bool, optional): [Indicates whether or not resultant Dataframes
        are to be saved]. Defaults to True.

    Returns:
        [DataFrame]: [Fully preprocessed]
    """
    # Ensures all tickers passed through are wrapped in a string for uniformity.
    if type(tickers) == str:
        # Sets counter so sleep only activates if needed.
        sleepy =len(tickers) - 1
        temp = tickers
        tickers = []
        tickers.append(temp)
    sleepy = len(tickers)
    # loops through ist of tickers, first using each ticker values to make API call,
    # then preprocessing.
    for ticker in tickers:
        # API calls
        data = API(ticker)
        # MACD signal
        data = crossover(data)
        # Sets start date
        data = alpha(data)
        # Sets end date
        data = omega(data, period)
        # drops an unecessary column
        data = dropcols(data)
        # fills NANs
        #TODO is this still necessary?
        data.fillna(method='bfill',inplace=True)
        # renames columns
        data = feature_names(data)
    # savess DataFrame to csv naming with date and ticker
    if save:
        data.to_csv(f'data/{period}-{ticker}.csv', mode='a', header=True)
    # API rate limit avoidance.
    if sleepy > 0:
        sleepy -=1
        sleep(7)
    return data
