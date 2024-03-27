import json
import os
import time
from web3 import Web3


web3 = Web3(Web3.HTTPProvider("https://api.developer.coinbase.com/rpc/v1/base/K6JT5NIkXJ7yyIh6Mtgxt6WJACLrPaN8"))

# The address of the UniswapV2 factory contract on base network
base_factory_address = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"
with open("abis/uniswapV2abi.json") as f:
    base_factory_contract_abi = json.load(f)
base_factory_contract = web3.eth.contract(address=base_factory_address, abi=base_factory_contract_abi)
#pair_created_filter = base_factory_contract.events.PairCreated.create_filter(fromBlock="latest")
latest_block = web3.eth.block_number

while True:
    # Get the new PairCreated events
    new_pairs = base_factory_contract.events.PairCreated.get_logs(fromBlock=latest_block) 

    for event in new_pairs:
        token0 = event['args']['token0']
        token1 = event['args']['token1']
        pair = event['args']['pair']

        print(f"New pair created: {token0}/{token1}, pair address: {pair}")

    time.sleep(30)  # wait for 60 seconds before the next check
