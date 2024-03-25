import ccxt
import pandas as pd
import pandas_ta as ta

exchange = ccxt.binance({
    'apiKey': 'f79ce8018b766cc715671af97d93394e28914413a5b98f916253af121f519e7e',
    'secret': 'b4a17b37259df7c4c701822a008f9c09a7021f56c07db4d77afc5839fb61f50e',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})
exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
markets = exchange.load_markets()

symbol = 'BTC/USDT'
timeframe = '1m'
amount =  0.01 # replace with your desired order amount
leverage = 10  # replace with your desired leverage
stop_loss_ratio = 1
take_profit_ratio = 1.5
order_created = False

while True:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        print('--------------------------------------------------------------')
        if len(ohlcv):
            df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')

            # Calculate MACD and EMA
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.ema(length=100, append=True)

            # Get the last row
            last_row = df.iloc[-1]

            print(df[-20:])
            print(exchange.iso8601(exchange.milliseconds()))
            print('--------------------------------------------------------------')

            # Check the conditions
            if last_row['MACD_12_26_9'] > last_row['MACDs_12_26_9'] and last_row['MACD_12_26_9'] < 0 and \
               last_row['MACDh_12_26_9'] > df.iloc[-2]['MACDh_12_26_9'] and last_row['close'] > last_row['EMA_100'] and \
               not order_created:
                # Create a market order
                order = exchange.create_market_buy_order(symbol, amount)

                # Set the stop loss and take profit prices
                stop_loss_price = last_row['EMA_100']
                take_profit_price = last_row['close'] * (1 + take_profit_ratio / 100)

                # Create a stop loss order
                stop_loss_order = exchange.create_order(symbol, 'stop_loss_limit', 'sell', amount, stop_loss_price, {'stopPrice': stop_loss_price})

                # Create a take profit order
                take_profit_order = exchange.create_order(symbol, 'take_profit_limit', 'sell', amount, take_profit_price, {'stopPrice': take_profit_price})

                print(f'Order created at price {last_row["close"]}')
                print(f'Stop loss order created at price {stop_loss_price}')
                print(f'Take profit order created at price {take_profit_price}')

                order_created = True
    except Exception as e:
        print(type(e).__name__, str(e))