# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import pandas_ta as ta
import pandas as pd
import ccxt
from dotenv import load_dotenv


# -----------------------------------------------------------------------------

print('CCXT Version:', ccxt.__version__)

# -----------------------------------------------------------------------------
# Load environment variables
load_dotenv()
#Exchange setup and connection API
exchange = ccxt.binance({
    'apiKey': os.getenv('TESTNET_BINANCE_API_KEY'),
    'secret': os.getenv('TESTNET_BINANCE_SECRET'),
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'future',
    },
})
#Exchange configuration
exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
markets = exchange.load_markets()

symbol = 'ETH/USDT'
timeframe = '1h'
limit = 500
rsi_length = 6
order_created = False
while True:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        print('--------------------------------------------------------------')
        if len(ohlcv):
            df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            df = pd.concat([df, df.ta.rsi(length=rsi_length)], axis=1)
            print(df[-20:])
            print(exchange.iso8601 (exchange.milliseconds()))

            print('--------------------------------------------------------------')
            #Check if the last RSI is less than 70
            if df.iloc[-1]['RSI_6'] > 70 and not order_created:
                # Fetch the current price of the symbol
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker['last'] 

                # Create a limit buy order
                order = exchange.create_limit_buy_order(symbol, 0.01, current_price)
                print(f'Order created at price {current_price}')

                order_created = True
    except Exception as e:
        print(type(e).__name__, str(e))

