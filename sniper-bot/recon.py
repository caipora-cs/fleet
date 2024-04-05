# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import json
import requests
from web3 import Web3
from goplus.token import Token

# Uniswap factory address
factory_address = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"


class Recon:
    """This class is responsible for monitoring the factory contract for new pairs."""

    def __init__(self, factory: str) -> None:
        self.factory = factory
        # Your RPC link connection
        self.web3 = Web3(
            Web3.HTTPProvider(
                "https://api.developer.coinbase.com/rpc/v1/base/K6JT5NIkXJ7yyIh6Mtgxt6WJACLrPaN8"
            )
        )
        with open("abis/uniswapV2abi.json", encoding="utf-8") as f:
            abi = json.load(f)
        self.contract = self.web3.eth.contract(address=factory, abi=abi)

    def get_new_pairs(self) -> None:
        """Logic to get new pairs from event logs in the factory contract"""
        latest_block = self.web3.eth.block_number
        new_pairs = self.contract.events.PairCreated.get_logs(fromBlock=latest_block)

        for event in new_pairs:
            token0 = event["args"]["token0"]
            token1 = event["args"]["token1"]
            pair = event["args"]["pair"]

            print(f"New pair created on UniV2: {token0}/{token1}, pair address: {pair}")
            # 0x4200000000000000000000000000000000000006 ignore weth in the pair for security check
            if token0 != "0x4200000000000000000000000000000000000006":
                token0_security_data = Token().token_security(
                    chain_id="8453", addresses=[token0]
                )
                print(f"Token0 security data: {token0_security_data}\n\n")

            if token1 != "0x4200000000000000000000000000000000000006":
                token1_security_data = Token().token_security(
                    chain_id="8453", addresses=[token1]
                )
                print(f"Token1 security data: {token1_security_data}\n\n")

    def screener(self,chain_id: str, pair_address: str):
        """
        Perform an API call to Dexscreener and retrieve information about a specific pair.
        """
        url= f"https://api.dexscreener.com/latest/dex/pairs/{chain_id}/{pair_address}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None



    # contract.events.PairCreated.get_logs(fromBlock=latest_block)
    # @property properties i might use for the Recon class
    # @cached_property for caching for repetitive calls ATT: if prop changed it will not be updated
    # @lru_cache for function calls

    def run(self) -> None:
        """Run function to continuously monitor for new pairs"""
        while True:
            self.get_new_pairs()


def main():
    """Main function to run the bot."""
    recon = Recon(factory_address)
    recon.run()


if __name__ == "__main__":
    main()
