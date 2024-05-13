import pandas as pd
from datetime import datetime
import pygsheets
from binance.client import Client
from config import API_KEY, API_SECRET
from adx import get_adx, algo_adx
import time
import asyncio

client = Client(API_KEY, API_SECRET)
# symbol = "BTCUSDT"
# exchange="Binance"
PERIOD_5M = Client.KLINE_INTERVAL_5MINUTE
PERIOD_15M = Client.KLINE_INTERVAL_15MINUTE
PERIOD_1H = Client.KLINE_INTERVAL_1HOUR
PERIOD_4H = Client.KLINE_INTERVAL_4HOUR
PERIOD_1D = Client.KLINE_INTERVAL_1DAY


class Get_data_binance:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_data(self):
        frame5m = pd.DataFrame(client.futures_historical_klines(self.symbol, PERIOD_5M, "700 minutes ago UTC"))
        frame15m = pd.DataFrame(client.futures_historical_klines(self.symbol, PERIOD_15M, "2100 minutes ago UTC"))
        frame1h = pd.DataFrame(client.futures_historical_klines(self.symbol, PERIOD_1H, "8400 minutes ago UTC"))
        frame4h = pd.DataFrame(client.futures_historical_klines(self.symbol, PERIOD_4H, "33600 minutes ago UTC"))
        frame1d = pd.DataFrame(client.futures_historical_klines(self.symbol, PERIOD_1D, "201600 minutes ago UTC"))

        frame5m = frame5m.iloc[:,:5]
        frame15m = frame15m.iloc[:,:5]
        frame1h = frame1h.iloc[:,:5]
        frame4h = frame4h.iloc[:,:5]
        frame1d = frame1d.iloc[:,:5]

        frame5m.columns = ['time', 'open', 'high', 'low', 'close']
        frame15m.columns = ['time', 'open', 'high', 'low', 'close']
        frame1h.columns = ['time', 'open', 'high', 'low', 'close']
        frame4h.columns = ['time', 'open', 'high', 'low', 'close']
        frame1d.columns = ['time', 'open', 'high', 'low', 'close']
        # frame['time'] = convert_to_gmt_plus_7(frame['time'])

        # Convert epoch to datetime 
        # frame['time'] = pd.to_datetime(frame['time'], unit='ms')
        # Convert to GMT+7 by adding 7 hours
        # frame['time'] = frame['time'] + timedelta(hours=7)

        frame5m = frame5m.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})
        frame15m = frame15m.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})
        frame1h = frame1h.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})
        frame4h = frame4h.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})
        frame1d = frame1d.astype({'open':'float64', 'high':'float64', 'low':'float64','close':'float64'})

        frame5m['DI+'] = pd.DataFrame(get_adx(frame5m['high'], frame5m['low'], frame5m['close'], 14)[0]).rename(columns = {0:'plus_di'})
        frame5m['DI-'] = pd.DataFrame(get_adx(frame5m['high'], frame5m['low'], frame5m['close'], 14)[1]).rename(columns = {0:'minus_di'})
        frame5m['ADX'] = pd.DataFrame(get_adx(frame5m['high'], frame5m['low'], frame5m['close'], 14)[2]).rename(columns = {0:'adx'})

        frame15m['DI+'] = pd.DataFrame(get_adx(frame15m['high'], frame15m['low'], frame15m['close'], 14)[0]).rename(columns = {0:'plus_di'})
        frame15m['DI-'] = pd.DataFrame(get_adx(frame15m['high'], frame15m['low'], frame15m['close'], 14)[1]).rename(columns = {0:'minus_di'})
        frame15m['ADX'] = pd.DataFrame(get_adx(frame15m['high'], frame15m['low'], frame15m['close'], 14)[2]).rename(columns = {0:'adx'})

        frame1h['DI+'] = pd.DataFrame(get_adx(frame1h['high'], frame1h['low'], frame1h['close'], 14)[0]).rename(columns = {0:'plus_di'})
        frame1h['DI-'] = pd.DataFrame(get_adx(frame1h['high'], frame1h['low'], frame1h['close'], 14)[1]).rename(columns = {0:'minus_di'})
        frame1h['ADX'] = pd.DataFrame(get_adx(frame1h['high'], frame1h['low'], frame1h['close'], 14)[2]).rename(columns = {0:'adx'})

        frame4h['DI+'] = pd.DataFrame(get_adx(frame4h['high'], frame4h['low'], frame4h['close'], 14)[0]).rename(columns = {0:'plus_di'})
        frame4h['DI-'] = pd.DataFrame(get_adx(frame4h['high'], frame4h['low'], frame4h['close'], 14)[1]).rename(columns = {0:'minus_di'})
        frame4h['ADX'] = pd.DataFrame(get_adx(frame4h['high'], frame4h['low'], frame4h['close'], 14)[2]).rename(columns = {0:'adx'})

        frame1d['DI+'] = pd.DataFrame(get_adx(frame1d['high'], frame1d['low'], frame1d['close'], 14)[0]).rename(columns = {0:'plus_di'})
        frame1d['DI-'] = pd.DataFrame(get_adx(frame1d['high'], frame1d['low'], frame1d['close'], 14)[1]).rename(columns = {0:'minus_di'})
        frame1d['ADX'] = pd.DataFrame(get_adx(frame1d['high'], frame1d['low'], frame1d['close'], 14)[2]).rename(columns = {0:'adx'})

        frame5m = frame5m.assign(cut_di = lambda x: (x['DI+'] - x['DI-']))
        frame15m = frame15m.assign(cut_di = lambda x: (x['DI+'] - x['DI-']))
        frame1h = frame1h.assign(cut_di = lambda x: (x['DI+'] - x['DI-']))
        frame4h = frame4h.assign(cut_di = lambda x: (x['DI+'] - x['DI-']))
        frame1d = frame1d.assign(cut_di = lambda x: (x['DI+'] - x['DI-']))

        # frame['cut_di'] = [cut_di(a, b) for a, b in zip(frame['DI+'], frame['DI-'])]
        
        frame5m = frame5m.sort_index(ascending=False)
        frame5m = frame5m.reset_index(drop=True)

        frame15m = frame15m.sort_index(ascending=False)
        frame15m = frame15m.reset_index(drop=True)

        frame1h = frame1h.sort_index(ascending=False)
        frame1h = frame1h.reset_index(drop=True)
        
        frame4h = frame4h.sort_index(ascending=False)
        frame4h = frame4h.reset_index(drop=True)

        frame1d = frame1d.sort_index(ascending=False)
        frame1d = frame1d.reset_index(drop=True)

        temp5m = frame5m.loc[0:0]
        temp15m = frame15m.loc[0:0]
        temp1h = frame1h.loc[0:0]
        temp4h = frame4h.loc[0:0]
        temp1d = frame1d.loc[0:0]

        temp5m['signal'] = algo_adx(frame5m)
        temp15m['signal'] = algo_adx(frame15m)
        temp1h['signal'] = algo_adx(frame1h)
        temp4h['signal'] = algo_adx(frame4h)
        temp1d['signal'] = algo_adx(frame1d)

        # temp = temp.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'DI+', 'DI-']).astype(str).values.tolist()
        temp5m = temp5m.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'ADX', 'DI+', 'DI-']).astype(str)
        temp15m = temp15m.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'ADX', 'DI+', 'DI-']).astype(str)
        temp1h = temp1h.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'ADX', 'DI+', 'DI-']).astype(str)
        temp4h = temp4h.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'ADX', 'DI+', 'DI-']).astype(str)
        temp1d = temp1d.drop(columns=['time', 'DI+', 'DI-', 'open', 'high', 'low', 'close', 'ADX', 'DI+', 'DI-']).astype(str)
        
        temp = pd.concat([temp5m, temp15m, temp1h, temp4h, temp1d], axis=1)
        temp.insert(0, "symbol", self.symbol)
        temp = temp.values.tolist()

        return temp


                                                 



