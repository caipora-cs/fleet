import ccxt
import pandas as pd
import numpy as np

exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('ETH/USDT', '1h')

df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Calculate the RSI
delta = df['close'].diff()
gain, loss = delta.copy(), delta.copy()
gain[gain < 0] = 0
loss[loss > 0] = 0
average_gain = gain.rolling(window=14).mean()
average_loss = abs(loss.rolling(window=14).mean())
rs = average_gain / average_loss
df['rsi'] = 100 - (100 / (1 + rs))

print(df)