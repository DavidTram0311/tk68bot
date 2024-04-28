import asyncio
import websockets
import json
import requests
import pandas as pd
from datetime import datetime
import pygsheets
from binance.client import Client
from config import API_KEY, API_SECRET
from datetime import timedelta
from adx import get_adx
import time
import os 
from function import return_adx, algo_adx, get_data


client = Client(API_KEY, API_SECRET)
cwd = os.getcwd()
# Authorization
gc = pygsheets.authorize(service_file=f'{cwd}\\creds.json')

client = Client(API_KEY, API_SECRET)
symbol = "BTCUSDT"
PERIOD_5_MIN = Client.KLINE_INTERVAL_5MINUTE
PERIOD_15_MIN = Client.KLINE_INTERVAL_15MINUTE


date = []
plus_di = []
minus_di = []
cut_di = []
adx = []
signal_futu = []
count = 0

while True:
    try:
        if datetime.now().minute % 5 == 0:
            time.sleep(58)
            count = count + 1
            print(f'Time: {count}')
            df = return_adx(get_data) # get adx indicator
            df = df.sort_index(ascending=False)
            df = df.reset_index(drop=True)
            signal = algo_adx(df) # get the signal
            futu = df.loc[0:0]
            futu['signal'] = signal

            # add values to tracker
            date.append(futu.iloc[0,0])
            plus_di.append(futu.iloc[0,5])
            minus_di.append(futu.iloc[0,6])
            adx.append(futu.iloc[0,7])
            cut_di.append(futu.iloc[0,8])
            signal_futu.append(futu.iloc[0,9])

            # drop values
            futu = futu.drop(columns=['open', 'high', 'low', 'close'])


            #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
            sh = gc.open('NAME OF DATA RAW SPREADSHEET')

            sc = gc.open('NAME OF BOT SIGNAL SPREADSHEET')

            #select the first sheet 
            wks = sh[0]

            wk = sc[0]

            #update the first sheet with df, starting at cell B2. 
            wks.set_dataframe(df,(0,0))
            wk.set_dataframe(futu,(0,0))

    except KeyboardInterrupt:
        print("Shut Down")
        dict = {'date': date, 
                'DI+': plus_di, 
                'DI-': minus_di,
                'ADX': adx,
                'cut_di':cut_di,
                'signal':signal_futu}
        
        tracker = pd.DataFrame(dict)
        tracker.to_csv(f'{datetime.now().strftime("%Y-%m-%d_%H%M")}-tracker.csv')
        break
