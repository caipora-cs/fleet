# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import json
from typing import Dict, List
from web3 import Web3
from goplus.token import Token
import requests

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

    def get_last_pairs(self, how_many: int = 10) -> List[Dict[str, str]]:
        """Get the last pairs created on the factory contract."""
        latest_block = self.web3.eth.block_number
        start_block = max(0, latest_block - 500)
        events = []

        while len(events) < how_many and start_block >= 0:
            new_events = self.contract.events.PairCreated.get_logs(
                fromBlock=start_block, toBlock=min(start_block + 500, latest_block)
            )
            events.extend(new_events)
            start_block -= 500

        last_events = events[-how_many:]
        pairs = []
        for event in last_events:
            token0 = event["args"]["token0"]
            token1 = event["args"]["token1"]
            pair = event["args"]["pair"]

            pairs.append({"token0": token0, "token1": token1, "pair": pair})

        return pairs

    def parse_pairs(self, pairs: List[Dict[str, str]]) -> List[str]:
        """Check which token is not WETH and return the list of them for security check."""
        non_weth_tokens = []
        weth_address = "0x4200000000000000000000000000000000000006"

        for pair in pairs:
            if pair["token0"] != weth_address:
                non_weth_tokens.append(pair["token0"])
            elif pair["token1"] != weth_address:
                non_weth_tokens.append(pair["token1"])

        return non_weth_tokens

    def check_security(self, pairs: List[str]):
        """Check the security properties of a list of pairs."""
        for pair in pairs:
            pair_security_data = Token().token_security(
                chain_id="8453", addresses=[pair]
            )
            print(pair_security_data)

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
            non_weth_token = (
                token0
                if token0 != "0x4200000000000000000000000000000000000006"
                else token1
            )
            token_security_data = Token().token_security(
                chain_id="8453", addresses=[non_weth_token]
            )
            print(f"Token security data: {token_security_data}\n\n")
            security = token_security_data.to_dict()
            if (
                non_weth_token in security["result"]
                and security["result"][non_weth_token]["is_open_source"] == "1"
            ):
                pair_data = self.screener(chain_id="base", pair_address=pair)
                print(json.dumps(pair_data, indent=4))
                if pair_data and pair_data["pair"]["liquidity"]["usd"] > 20000:
                    print("PREPARE TO BUY")

    def screener(self, chain_id: str, pair_address: str):
        """
        Perform an API call to Dexscreener and retrieve information about a specific pair.
        """
        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain_id}/{pair_address}"
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

    def run(self, iterations: int = 30) -> None:
        """Run function to continuously monitor for new pairs"""
        for _ in range(iterations):
            self.get_new_pairs()


def main():
    """Main function to run the bot."""
    recon = Recon(factory_address)
    # recon.run()
    pairs = recon.get_last_pairs()
    non_weth_pairs = recon.parse_pairs(pairs)
    recon.check_security(non_weth_pairs)


if __name__ == "__main__":
    main()
