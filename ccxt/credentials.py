# -*- coding: utf-8 -*-
import ccxt
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
print('CCXT Version:', ccxt.__version__)

exchange = ccxt.binance({
    'apiKey': os.getenv('TESTNET_BINANCE_API_KEY'),
    'secret': os.getenv('TESTNET_BINANCE_SECRET'),
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'future',
    },
})

exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
markets = exchange.load_markets()
exchange.verbose = True  # debug output

balance = exchange.fetch_balance()
positions = balance['info']['positions']

# look for availableBalance on output.md
pprint(positions)