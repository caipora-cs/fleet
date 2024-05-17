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


Para melhorar a performance do script:

1. **Evite operações desnecessárias**: Se você está realizando a mesma operação várias vezes, considere armazenar o resultado em uma variável e reutilizá-la.

2. **Use estruturas de dados eficientes**: Dependendo do seu caso de uso, diferentes estruturas de dados podem ter melhor desempenho. Por exemplo, se você precisa verificar se um item está em uma lista, um conjunto (`set`) é mais eficiente do que uma lista (`list`).

3. **Paralelização**: Se você está processando uma grande quantidade de dados e cada peça de dados pode ser processada independentemente, você pode ser capaz de usar paralelização para dividir o trabalho entre vários núcleos de CPU ou até mesmo várias máquinas.

4. **Profiling**: Use ferramentas de profiling para identificar as partes do seu código que estão levando mais tempo. Isso pode ajudá-lo a focar seus esforços de otimização onde eles terão o maior impacto.

5. **Evite bloqueios desnecessários**: Se o seu código está esperando por I/O (como uma solicitação de rede), considere se você pode fazer essa espera de forma assíncrona para que seu código possa continuar fazendo trabalho útil enquanto espera.

6. **Caching**: Se você está fazendo solicitações de rede ou consultas de banco de dados que retornam os mesmos resultados repetidamente, considere usar um cache para armazenar os resultados e reutilizá-los.

No seu caso específico, parece que você está fazendo várias solicitações de rede (`recon.screener_by_token`). Se essas solicitações são independentes, você pode ser capaz de paralelizá-las para melhorar o desempenho. Além disso, se você está fazendo as mesmas solicitações repetidamente, um cache pode ser útil.


Fleet: The Sniper Bot is a sophisticated trading automator designed for the blockchain environment. Its primary purpose is to automate your trading strategies, allowing for a hands-off approach to cryptocurrency trading. By leveraging the programmability of blockchain technology, the bot can execute trades based on predefined conditions and strategies, eliminating the need for manual intervention.

Blockchain programmability refers to the ability to write code (smart contracts) that runs directly on the blockchain. This code can automate complex transactions, create decentralized applications, and much more. It's a powerful feature that opens up a world of possibilities for automating financial transactions and creating decentralized applications.

Automating your trading strategies with a tool like Fleet: The Sniper Bot can be highly beneficial. It allows you to execute trades 24/7, react to market conditions more quickly than a human could, and eliminate emotional decision-making from your trading. Furthermore, the bot is designed to be self-sustaining, auto-healing, and auto-scaling, meaning it can adapt to changing market conditions, recover from failures, and handle increasing load as your trading volume grows.

