##### TODO:

- Design Database for transaction log
    - Its gonna be a AWS dynamoDB running lambda functions
- Docker aplication bundling for cloud
- Refactor code into OOP
- Backtesting ccxt on old Data
- Gathering data from uniswap for backtesting sniper module
    - Develop python data analysis module to determine signals for the bot

Sniper Features:
- Add a feature to the bot to buy and sell on a specific signal:
    -signals:
        - BUY:
            - 2min from pair creation 
            - Open source and security audited by goplus 
            - Run data analysis on agregated newPairs data for more signals
        - SELL:    
            - 20% to 50% profit ratio (determine from backtesting)
            - 5 min from creation (determine from backtesting)
            - find a way to determine wich ones are long term holders
                - Scrape a website/ telegram/ twitter for the coin
        -HOLD:
            - Make a mini script that check the coin DexScreener page for a website span

- Add api calls to the bot for controlling it on the cloud   
    - API Gateway
    - FastAPI
- Prepare it for cloud deployment
- Handle errors and exceptions that might occur during buying and selling

recon.py:
    - Right now the bot returns one batch of the last N events
    - Try a loop where it gets the last 10 events every 10 seconds
        - Run all the necessary checks
        - Return the coins that are good
        - Save security and screnner info about this coins on DB
    - Create a module where it goes and get updated info on the coins already in the DB after 10 min, 1h, 1d, 1w and add to the info already there

    My data squema for the DB:
    {
        "pairId": "0xaFafFc47072FD2ac75e15D0CA4700852e293725f",
        "tokens": ["0x92Ea8f2b711076cC08a734a8e9cD57D3963EbfFf", "0x4200000000000000000000000000000000000006"],
        "token0": "0x92Ea8f2b711076cC08a734a8e9cD57D3963EbfFf",
        "token1": "0x4200000000000000000000000000000000000006",
        "security": {
            "transfer_pausable": "0",
            "trust_list": None
        },
        "name": "🐕 Base REX",
        "symbol": "BREX",
        "fdv": 18594,
        "liquidity_usd": 18611.19,
        "creation_timestamp": 1714043589000,
        "price_change": {
            "h1": 0,
            "h24": 0,
            "h6": 0,
            "m5": 0
        },
        "volume": {
            "h1": 0.92,
            "h24": 0.92,
            "h6": 0.92,
            "m5": 0
        },
        "time_scanned": "2024-04-25 12:13:09",
        "buy_signal": false
        "website": "https://www.brex.com"
    }

Monitoring and Logging
    -CloudWatch