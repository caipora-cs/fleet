import ccxt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
exchange = ccxt.binance(
    {
        "apiKey": os.getenv("TESTNET_BINANCE_API_KEY"),
        "secret": os.getenv("TESTNET_BINANCE_SECRET"),
        "enableRateLimit": True,
        "options": {
            "defaultType": "future",
        },
    }
)
exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
markets = exchange.load_markets()

symbol = "BTC/USDT"
timeframe = "1m"
amount = 0.01  # replace with your desired order amount
leverage = 10  # replace with your desired leverage
stop_loss_ratio = 1
take_profit_ratio = 1.5
order_created = False

while True:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        print("--------------------------------------------------------------")
        if len(ohlcv):
            df = pd.DataFrame(
                ohlcv, columns=["time", "open", "high", "low", "close", "volume"]
            )
            df["time"] = pd.to_datetime(df["time"], unit="ms")

            # Calculate MACD and EMA
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.ema(length=100, append=True)

            # Get the last row
            last_row = df.iloc[-1]

            print(df[-20:])
            print(exchange.iso8601(exchange.milliseconds()))
            print("--------------------------------------------------------------")

            # Check the conditions
            if (
                last_row["MACD_12_26_9"] > last_row["MACDs_12_26_9"]
                and last_row["MACD_12_26_9"] < 0
                and last_row["MACDh_12_26_9"] > df.iloc[-2]["MACDh_12_26_9"]
                and last_row["close"] > last_row["EMA_100"]
                and not order_created
            ):
                # Create a market order
                order = exchange.create_market_buy_order(symbol, amount)
                print(f'Order created at price {last_row["close"]}')

                # Set the stop loss and take profit prices
                stop_loss_price = last_row["EMA_100"]
                take_profit_price = last_row["close"] * (1 + take_profit_ratio / 100)

                # Create a stop loss order
                stop_loss_order = exchange.create_order(
                    symbol,
                    "limit",
                    "sell",
                    amount,
                    stop_loss_price,
                    {"stopPrice": stop_loss_price},
                )
                print(f"Stop loss order created at price {stop_loss_price}")

                # Create a take profit order
                take_profit_order = exchange.create_order(
                    symbol,
                    "limit",
                    "sell",
                    amount,
                    take_profit_price,
                    {"stopPrice": take_profit_price},
                )
                print(f"Take profit order created at price {take_profit_price}")

                order_created = True
    except Exception as e:
        print(type(e).__name__, str(e))
