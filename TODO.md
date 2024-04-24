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

Monitoring and Logging
    -CloudWatch