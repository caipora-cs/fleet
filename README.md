[![My Skills](https://skillicons.dev/icons?i=linux,aws,dynamodb,kubernetes,obsidian,py,solidity,)](https://skillicons.dev)

<div align= "center">
<svg height="40" width="200" xmlns="http://www.w3.org/2000/svg">
  <text x="5" y="30" fill="none" stroke="pink" font-size="35">fleet</text>
</svg>
</div> 
---

The trading bot operates by monitoring decentralized exchanges (DEX) and centralized exchanges (CEX) to identify new token pairs, assess their security, and execute trades based on predefined conditions. The bot is designed to work with Uniswap on the DEX side and Binance on the CEX side, utilizing the ccxt library for API calls to Binance.

To understand how our sniper bot strategy works on Uniswap, it's important to grasp the basics of how Uniswap operates. Uniswap, a popular decentralized exchange, relies on three main smart contracts: Factory, Pair, and Router.

#### Uniswap's Main Smart Contracts:

1. **Factory Contract**:
    - This contract is responsible for creating and managing liquidity pools. When a new liquidity pool is created, it generates a unique contract for that pool and issues LP (Liquidity Provider) tokens to the providers.
2. **Pair Contract**:
    - The Pair contract keeps track of the balances of the two tokens in the liquidity pool. It also implements the Automated Market Maker (AMM) logic, which determines the prices of the tokens based on their supply and demand in the pool.
3. **Router Contract**:
    - The Router contract is the main interface for interacting with Uniswap. It allows users to swap tokens and add or remove liquidity from pools. When you use Uniswap, you're typically interacting with the Router contract.

#### Tech Stack

1. **Programming Language**: Python
2. **Libraries and Frameworks**:
    - `ccxt`: For interfacing with Binance API.
    - `web3.py`: For interacting with Ethereum blockchain.
    - `requests`: For making API requests to the security and .
    - `pprint`: Formatting output.
    - `boto3`: Connector to AWS services.
    - `goplus:` Security API
    - `dotenv:` For enviroment variables needed for AWS ans Wallet secrets
1. **Database**: AWS DynamoDB for backend data analysis and storage.
2. **Cache**: DAX or ElasticCache (AWS)
3. **Other Dependencies**: Specified in the `pyproject.toml` for Poetry.

#### Reasoning and Logic

The bot follows a systematic approach:

1. **Monitoring**: Constantly monitors new token pairs created on Uniswap using smart contract events.
2. **Security Checks**: Evaluates the security of these new tokens to avoid scams and ensure reliability.
3. **Trading Signals**: Based on the analysis, generates buy signals for tokens that meet specific criteria.
4. **Execution**: Executes trades automatically if the security checks are passed and the profit ratio condition is met.
5. **Backtesting**: Utilizes historical data stored in AWS DynamoDB for backtesting strategies.

#### Requirements

1. **Python 3.7+**.
2. **Web3.py** for Ethereum interaction.
3. **ccxt** for Binance API interaction.
4. **AWS DynamoDB** setup for storing and analyzing historical data.
5. **RPC node access** for interacting with Ethereum blockchain.


#### Recon Module
The `Recon` class is responsible for monitoring the Uniswap factory contract for new token pairs and performing initial security checks.

   ```python
   class Recon:
       def __init__(self, factory: str) -> None:
           self.factory = factory
           self.w3 = rpc()
           self.contract = self.w3.eth.contract(address=factory, abi=factory_abi)
           self.contract_v3 = self.w3.eth.contract(address=factory_address_v3, abi=factory_abi_v3)
       
       def get_last_pairs(self, how_many: int = 10) -> List[Dict[str, str]]:
           # Logic to fetch last pairs
           pass
       
       def get_last_pairs_v3(self, how_many: int = 10) -> List[Dict[str, str]]:
           # Logic to fetch last pairs for Uniswap V3
           pass
       
       def parse_pairs(self, pairs: List[Dict[str, str]]) -> List[str]:
           # Logic to parse pairs and filter non-WETH tokens
           pass
       
       def check_security(self, pairs: List[str]) -> List[Dict]:
           # Logic to check security of tokens
           pass
       
       def get_new_pairs(self) -> None:
           # Logic to get new pairs and print details
           pass
       
       def get_open_source(self, security_data_objects: List[Dict]) -> List[Dict]:
           # Logic to filter open source tokens
           pass
       
       def screener_by_pair(self, chain_id: str, pair_address: str) -> json:
           # API call to Dexscreener
           pass
       
       def screener_by_token(self, token_addreses: str) -> json:
           # API call to Dexscreener for a specific token
           pass
       
       def run(self, iterations: int = 30) -> None:
           # Continuously monitor for new pairs
           pass
       
       def create_token_data(self, security_data_object, token_data):
           # Create a TokenData object for storage
           pass
   ```

#### Txn Module
The `Txn` module handles the execution of trades on both the CEX and DEX. It uses the `ccxt` library for CEX and web3 for DEX interactions.
The `txns.py`  is designed to facilitate automated trading on the Ethereum blockchain, specifically through Uniswap. The script handles various aspects of interacting with Ethereum smart contracts, including token purchases and sales, gas estimation, and transaction management.

This module provides a robust foundation for automated trading on Uniswap. It includes critical functionalities like buying and selling tokens, gas estimation, and transaction management, all with extensive error handling and dynamic configurations. The modular design and clear method definitions make it easy to extend and customize further.

Here's a detailed breakdown of the `txns.py` module:

##### Key Classes and Functions

1. **EthereumAddress Class**
    
    - Validates and handles Ethereum addresses.
    - Ensures the address is valid and checksummed.
2. **Transaction Class**
    
    - Manages the buying and selling of tokens.
    - Contains functions to set up token contracts, gas parameters, and addresses.
    - Handles transaction building, signing, sending, and receipt waiting.
    - Includes methods for checking allowances, estimating gas, and getting token information.

##### Enhancements and Error Handling

1. **Improved Error Handling**:
    
    - The script includes detailed error handling for different exceptions such as `ValueError`, `TransactionNotFound`, and `TimeExhausted`.
2. **Gas Estimation**:
    
    - The gas estimation method (`estimate_gas`) calculates the gas required for transactions and checks if it exceeds the user's set maximum gas limit.
3. **Dynamic Configurations**:
    
    - The script loads settings dynamically from a configuration file (`settings.json`), making it adaptable to different environments and user preferences.

3. **Supportive Utility Modules**

   - **connect.py**: Manages RPC connections and contract addresses.
   - **style.py**: Handles output styling for console logs.
   - **token.py**: Contains logic for token security checks using GoPlus API.

#### Workflow

1. **Recon Module**:
   - Fetch last pairs from Uniswap V2 and V3.
   - Parse pairs to identify non-WETH tokens.
   - Check the security of identified tokens.
   - Filter open source tokens.
   - Retrieve token data from Dexscreener.
   - Create and store token data if criteria are met.

2. **Txn Module**:
   - Place orders on Binance.
   - Execute trades based on signals generated from Recon module.

#### Poetry Requirements

Dependencies are managed using Poetry. Example `pyproject.toml` configuration:

```toml
[tool.poetry]
name = "fleet"
version = "0.1.0"
description = "A multi-modular trading bot"
authors = ["caipora"]
license = "MIT"
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = "^3.12"
requests = "^2.31.0"
goplus = "^0.2.3"
python-dotenv = "^1.0.1"
web3 = "^6.16.0"
boto3 = "^1.34.95"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### Back-End:
**DynamoDB**
This script demonstrates how to programmatically create and configure a DynamoDB table with auto-scaling capabilities using Python and Boto3. It's a foundational piece for applications that require a scalable, serverless database backend on AWS.

```python
import boto3
import dataclasses
# from botocore.exceptions import ClientError
from sniper_bot.utils.style import style
from sniper_bot.models.token_model import TokenData

class DynamoDB:

def __init__(self) -> None:

self.dynamodb = boto3.resource("dynamodb")
self.client = boto3.client() 
# The AWS SDK for Python (Boto3) to make connections
self.table = self.dynamodb.Table("TokenData")

def create_table(self):

"""Create the TokenData table in DynamoDB. It will provision a scalable read and write capacity."""

# Wait until the table exists.
# Define the autoscaling for read capacity
# Define the autoscaling for write capacity
# Define autoscaling policy for read capacity
# Define autoscaling policy for write capacity

# CRUD operations

def create_item(self, token_data: TokenData):
def read_item(self, pair_id: str):
def update_item(self, pair_id: str, token_data: TokenData):
def delete_item(self, pair_id: str):

# Main Logic
def main():
db = DynamoDB()
# Create the table in DynamoDB for first time
db.create_table()  
if __name__ == "__main__":
main()
```