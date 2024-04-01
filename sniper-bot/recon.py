# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import json
import time
from web3 import Web3


web3 = Web3(
    Web3.HTTPProvider(
        "https://api.developer.coinbase.com/rpc/v1/base/K6JT5NIkXJ7yyIh6Mtgxt6WJACLrPaN8"
    )
)
latest_block = web3.eth.block_number
#Uniswap factory address
factory_address = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"
class Recon:
    """This class is responsible for monitoring the factory contract for new pairs."""
    def __init__(self, factory: str) -> None:
        self.factory = factory
        with open("abis/uniswapV2abi.json", encoding="utf-8") as f:
            abi = json.load(f)
        self.contract = web3.eth.contract(
            address=factory, abi=abi
        )

def main():
    """Main function to run the bot."""
    recon = Recon(factory_address)
    while True:
        # Get the new PairCreated events
        new_pairs = recon.contract.events.PairCreated.get_logs(
            fromBlock=latest_block
        )

        for event in new_pairs:
            token0 = event["args"]["token0"]
            token1 = event["args"]["token1"]
            pair = event["args"]["pair"]

            print(f"New pair created: {token0}/{token1}, pair address: {pair}")

        time.sleep(30)  # wait for 60 seconds before the next check

if __name__ == "__main__":
    main()
