import pandas as pd
import numpy as np
import requests


def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]    
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()
    
    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()
    return plus_di, minus_di, adx_smooth

def algo_adx(df):
    # last > 0 # Singal: Long
    if df.iloc[0,8] > 0:
        if df.iloc[0,7] > df.iloc[1,7]:
            return "LONG NOW"
        else:
            return "CONSIDER LONG"

    # last < 0 # Singal: Short  
    elif df.iloc[0,8] < 0:
        if df.iloc[0,7] > df.iloc[1,7]:
            return "SHORT NOW"
        else:
            return "CONSIDER SHORT"
