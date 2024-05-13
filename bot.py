from adx import algo_adx
import pandas as pd 
from adx import get_adx
from datetime import timedelta
from binance.client import Client
from config import API_KEY, API_SECRET
from datetime import datetime
import pygsheets
import os
import time
from function import Get_data_binance 

client = Client(API_KEY, API_SECRET)
cwd = os.getcwd()
# Authorization
gc = pygsheets.authorize(service_file=f'{cwd}\\creds.json')

client = Client(API_KEY, API_SECRET)
PERIOD_5M = Client.KLINE_INTERVAL_5MINUTE
PERIOD_15M = Client.KLINE_INTERVAL_15MINUTE
PERIOD_1H = Client.KLINE_INTERVAL_1HOUR
PERIOD_4H = Client.KLINE_INTERVAL_4HOUR
PERIOD_1D = Client.KLINE_INTERVAL_1DAY

# Read Coin List
coins = pd.read_csv(f'{cwd}\\coin_list.csv')
coins=coins.drop(columns=['Unnamed: 0'])

# Main
sc = gc.open('ADX-BOT')
wk = sc[1]

start_time = time.time()
start_date = datetime.now()

print(f"Start program: {start_date}")

count_exe = 0

while True:
    try:
        count_exe = count_exe + 1

        print(f"Start {count_exe} times: {datetime.now()}")
        data = Get_data_binance('BTCUSDT')
        # data = Get_data_binance(coins['symbol'][0])
        temp = data.get_data()

        count = 1
        print(count)

        try:
            for coin in range(len(coins['symbol'])):
                print(f'Check 1: {coins["symbol"][coin]}')
                data = Get_data_binance(coins['symbol'][coin])

                temp1 = data.get_data()
                temp = temp + temp1

                if coins["symbol"][coin + 1] == 'QNTUSDT':
                    time.sleep(1)
                count = count + 1
                print(f'Checkpoint 2: {count}')
                
            wk.update_values(f'C5', temp)
            
        except:
            print(f'End {count_exe} times: {datetime.now()} after {time.time() - start_time}')
            # Update signal into sheet
            wk.update_values(f'C5', temp)
        
        time.sleep(10)

    except KeyboardInterrupt:
        wk.update_values(f'C5', temp)
        print(f'Finish {count_exe} times: {datetime.now()} after {time.time() - start_time}')
        break


