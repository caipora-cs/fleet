# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import pandas_ta as ta
import pandas as pd
import ccxt

# -----------------------------------------------------------------------------

print('CCXT Version:', ccxt.__version__)

# -----------------------------------------------------------------------------

#Exchange setup and connection API
exchange = ccxt.binance({
    'apiKey': 'f79ce8018b766cc715671af97d93394e28914413a5b98f916253af121f519e7e',
    'secret': 'b4a17b37259df7c4c701822a008f9c09a7021f56c07db4d77afc5839fb61f50e',
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

