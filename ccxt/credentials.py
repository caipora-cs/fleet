# -*- coding: utf-8 -*-
import ccxt
from pprint import pprint

print('CCXT Version:', ccxt.__version__)

exchange = ccxt.binance({
    'apiKey': 'f79ce8018b766cc715671af97d93394e28914413a5b98f916253af121f519e7e',
    'secret': 'b4a17b37259df7c4c701822a008f9c09a7021f56c07db4d77afc5839fb61f50e',
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