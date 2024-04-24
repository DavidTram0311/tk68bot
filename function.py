import pandas as pd
from datetime import datetime
import pygsheets
from binance.client import Client
from datetime import timedelta
from config import API_KEY, API_SECRET
from adx import get_adx
import time

client = Client(API_KEY, API_SECRET)
symbol = "BTCUSDT"
PERIOD_5_MIN = Client.KLINE_INTERVAL_5MINUTE
PERIOD_15_MIN = Client.KLINE_INTERVAL_15MINUTE

# Function to convert epoch to GMT+7
def convert_to_gmt_plus_7(timestamps):
    # Convert epoch to datetime 
    datetime_objects = pd.to_datetime(timestamps, unit='ms')
    
    # Convert to GMT+7 by adding 7 hours
    datetime_objects_gmt_plus_7 = datetime_objects + timedelta(hours=7)
    
    return datetime_objects_gmt_plus_7


def get_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval,  lookback + " day ago UTC"))
    frame = frame.iloc[:,:5]
    frame.columns = ['time', 'open', 'high', 'low', 'close']
    frame['time'] = convert_to_gmt_plus_7(frame['time'])
    frame = frame.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})
    # frame = frame.set_index('time')
    # frame = frame.astype(float)
    return frame

def cut_di(plus_di, minus_di):
    return plus_di - minus_di

def return_adx(get_data):
    df = get_data("BTCUSDT", PERIOD_5_MIN, '1')
    df['DI+'] = pd.DataFrame(get_adx(df['high'], df['low'], df['close'], 14)[0]).rename(columns = {0:'plus_di'})
    df['DI-'] = pd.DataFrame(get_adx(df['high'], df['low'], df['close'], 14)[1]).rename(columns = {0:'minus_di'})
    df['ADX'] = pd.DataFrame(get_adx(df['high'], df['low'], df['close'], 14)[2]).rename(columns = {0:'adx'})

    df['cut_di'] = [cut_di(a, b) for a, b in zip(df['DI+'], df['DI-'])]

    return df

def algo_adx(df):
    # last > 0
    if df.iloc[0,8] > 0:
        if df.iloc[0,8] > df.iloc[1,8] and df.iloc[1,8] < 0:
            if df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] < 0:
                return "LONG"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "LONG"
            elif df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "LONG"
            
        elif df.iloc[0,8] > df.iloc[1,8] and df.iloc[1,8] > 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "LONG"
            elif df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] > 0:
                return "LONG"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "LONG"
            
        elif df.iloc[0,8] < df.iloc[1,8] and df.iloc[1,8] > 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "LONG"
            elif df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] > 0:
                return "LONG"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "CONSIDER LONG" 

    # last < 0     
    elif df.iloc[0,8] < 0:
        if df.iloc[0,8] < df.iloc[1,8] and 0 < df.iloc[1,8] < 1 and -1 < df.iloc[0,8] < 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "LONG"
            
        elif df.iloc[0,8] < df.iloc[1,8] and df.iloc[1,8] > 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] > 0:
                return "CONSIDER SHORT"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "CONSIDER SHORT"
            elif df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "CONSIDER SHORT"
            
        elif df.iloc[0,8] < df.iloc[1,8] and df.iloc[1,8] < 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "SHORT"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] < 0:
                return "SHORT"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "SHORT"
            
        elif df.iloc[0,8] > df.iloc[1,8] and df.iloc[1,8] < 0:
            if df.iloc[1,8] > df.iloc[2,8] and df.iloc[2,8] < 0:
                return "SHORT"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] < 0:
                return "SHORT"
            elif df.iloc[1,8] < df.iloc[2,8] and df.iloc[2,8] > 0:
                return "SHORT"
            