# core imports
from datetime import datetime
import numpy as np
import pandas as pd
from time import sleep


# Aplhavantage
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

tickers = ['AAPL','ACN','ADBE','ADI','ADP','ADSK','AKAM','AMAT','AMD','ANET','ANSS','APH','AVGO','BR','CDNS','CDW','CRM','CSCO','CTSH','CTXS','DXC','ENPH','FFIV','FIS','FISV','FLIR','FLT','FTNT','GLW','GPN','HPE','HPQ','IBM','INTC','INTU','IPGP','IT','JKHY','JNPR','KEYS','KLAC','LRCX','MA','MCHP','MPWR','MSFT','MSI','MU','MXIM','NLOK','NOW','NTAP','NVDA','NXPI','ORCL','PAYC','PAYX','PYPL','QCOM','QRVO','SNPS','STX','SWKS','TEL','TER','TRMB','TXN','TYL','V','VRSN','WDC','WU','XLNX','ZBRA']
# tickers = ['AAPL','ACN']

def API(ticker):
    API_key = 'CSMN0LYTQ5UYMVUT'
    API_URL = "https://www.alphavantage.co/query"
    
    
    ts = TimeSeries(key=API_key, output_format='pandas')
    price = ts.get_daily_adjusted(ticker, outputsize='full')[0]
    
    
    
    ti = TechIndicators(key=API_key, output_format='pandas')
    
    macd, meta_data = ti.get_macd(symbol=ticker,interval='daily')
    bbands, meta_data = ti.get_bbands(symbol=ticker,interval='daily')
    rsi,meta_data = ti.get_rsi(symbol=ticker,interval='daily',time_period=15)
    sma5, meta_data = ti.get_sma(symbol=ticker,time_period=5)
    sma15, meta_data = ti.get_sma(symbol=ticker,time_period=15)
    roc, meta_data = ti.get_roc(symbol=ticker,series_type='high',interval='daily')
    cci, meta_data = ti.get_cci(symbol=ticker,time_period=60,interval='daily')
    dx, meta_data = ti.get_dx(symbol=ticker,time_period=60,interval='daily')
    
    data = pd.concat([price, macd, bbands, rsi, sma5, sma15, roc, cci, dx], axis=1)
    data = data.dropna()
    data['ticker'] = ticker
    return data
    

def crossover(data):
    data['crossover'] = data['MACD'] > data['MACD_Signal']
    return data
def cutoff(data):
    return data[data.index>=datetime(2015, 1, 1)]
def dropcols(data):
    data = data.drop(columns=['4. close', '7. dividend amount', '8. split coefficient'])
    return data
def feature_names(data):
    data = data.rename(columns={'1. open':'open', '2. high':'high', '3. low':'low', '5. adjusted close':'adjc', '6. volume':'vol'})
    return data

def preprocess_data(tickers):
    for ticker in tickers:
        data = API(ticker)
        data = crossover(data)
        data = cutoff(data)
        data = dropcols(data)
        data.fillna(method='bfill',inplace=True)
        data = feature_names(data)
        data.to_csv('data/data.csv', mode='a', header=True)
    sleep(7)    
    pass



#activator
df = pd.read_csv('data/data.csv')