# pylint: disable=invalid-name
import requests
import json
import pprint
from datetime import datetime, timedelta
from typing import Dict, List
from goplus.token import Token
from connect import connect as rpc
from connect import (
    factory_address,
    factory_abi,
    factory_address_v3,
    factory_abi_v3,
)
from models.token_model import TokenData, Volume, Security, PriceChange


class Recon:
    """This class is responsible for monitoring the factory contract for new pairs."""

    def __init__(self, factory: str) -> None:
        self.factory = factory
        # Your RPC link connection
        self.w3 = rpc()
        self.contract = self.w3.eth.contract(address=factory, abi=factory_abi)
        self.contract_v3 = self.w3.eth.contract(
            address=factory_address_v3, abi=factory_abi_v3
        )

    def get_last_pairs(self, how_many: int = 10) -> List[Dict[str, str]]:
        """Get the last pairs created on the factory contract."""
        latest_block = self.w3.eth.block_number
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

    def get_last_pairs_v3(self, how_many: int = 10) -> List[Dict[str, str]]:
        """Get the last pairs created on the factory contract. This one uses Pools for Uniswap V3 factory arquiteture."""
        latest_block = self.w3.eth.block_number
        start_block = max(0, latest_block - 500)
        events = []

        while len(events) < how_many and start_block >= 0:
            new_events = self.contract_v3.events.PoolCreated.get_logs(
                fromBlock=start_block, toBlock=min(start_block + 500, latest_block)
            )
            events.extend(new_events)
            start_block -= 500

        last_events = events[-how_many:]
        pools = []
        for event in last_events:
            token0 = event["args"]["token0"]
            token1 = event["args"]["token1"]
            pool = event["args"]["pool"]

            pools.append({"token0": token0, "token1": token1, "pool": pool})

        return pools

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

    def check_security(self, pairs: List[str]) -> List[Dict]:
        """Check the security properties of a list of pairs."""
        security_data_objects = []
        for pair in pairs:
            pair_security_data = Token().token_security(
                chain_id="8453", addresses=[pair]
            )
            security_data_objects.append(pair_security_data)
        return security_data_objects

    def get_new_pairs(self) -> None:
        """Logic to get new pairs from event logs in the factory contract"""
        latest_block = self.w3.eth.block_number
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
                pair_data = self.screener_by_pair(chain_id="base", pair_address=pair)
                print(json.dumps(pair_data, indent=4))
                if pair_data and pair_data["pair"]["liquidity"]["usd"] > 20000:
                    print("PREPARE TO BUY")

    def get_open_source(self, security_data_objects: List[Dict]) -> List[Dict]:
        """Get the open source objects from the security data objects."""
        open_source_objects = []
        for data in security_data_objects:
            data_dict = data.to_dict()
            if data_dict["result"]:  # if the result is not empty
                token_address = list(data_dict["result"].keys())[0]
                if data_dict["result"][token_address]["is_open_source"] == "1":
                    open_source_objects.append(data_dict)
        return open_source_objects

    def screener_by_pair(self, chain_id: str, pair_address: str) -> json:
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

    def screener_by_token(self, token_addreses: str) -> json:
        """
        Perform an API call to Dexscreener and retrieve information about a specific pair.
        """
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token_addreses}"
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

    def create_token_data(self, security_data_object, token_data):
        """Create a TokenData object from the security_data_object and token_data. For storing porpuses."""
        # Extract the necessary information from the security_data_object
        token_address = list(security_data_object["result"].keys())[0]
        security_info = security_data_object["result"][token_address]
        security = Security(
            is_airdrop_scam=security_info["is_airdrop_scam"],
            is_anti_whale=security_info["is_anti_whale"],
            is_blacklisted=security_info["is_blacklisted"],
            is_honeypot=security_info["is_honeypot"],
            is_in_dex=security_info["is_in_dex"],
            is_mintable=security_info["is_mintable"],
            is_proxy=security_info["is_proxy"],
            is_whitelisted=security_info["is_whitelisted"],
            sell_tax=security_info["sell_tax"],
            trading_cooldown=security_info["trading_cooldown"],
            transfer_pausable=security_info["transfer_pausable"],
        )

        # Extract the necessary information from the token_data
        pair_info = token_data["pairs"][0]
        price_change = PriceChange(
            h1=pair_info["priceChange"]["h1"],
            h24=pair_info["priceChange"]["h24"],
            h6=pair_info["priceChange"]["h6"],
            m5=pair_info["priceChange"]["m5"],
        )
        volume = Volume(
            h1=pair_info["volume"]["h1"],
            h24=pair_info["volume"]["h24"],
            h6=pair_info["volume"]["h6"],
            m5=pair_info["volume"]["m5"],
        )

        # Create the TokenData object
        token_data = TokenData(
            pair_id=pair_info["pairAddress"],
            tokens=[
                pair_info["baseToken"]["address"],
                pair_info["quoteToken"]["address"],
            ],
            token0=pair_info["baseToken"]["address"],
            token1=pair_info["quoteToken"]["address"],
            security=security,
            name=pair_info["baseToken"]["name"],
            symbol=pair_info["baseToken"]["symbol"],
            fdv=pair_info["fdv"],
            liquidity_usd=pair_info["liquidity"]["usd"],
            creation_timestamp=datetime.fromtimestamp(
                pair_info["pairCreatedAt"] / 1000.0
            ),
            price_change=price_change,
            volume=volume,
            time_scanned=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            buy_signal=pair_info["liquidity"]["usd"] > 20000,
            website=pair_info["url"],
        )

        return token_data


def main():
    """Main function to run the bot."""
    # instantiate the Recon class
    recon = Recon(factory_address)
    pp = pprint.PrettyPrinter(indent=4)
    # recon.run() #uncomment this line to run the bot in real time monitoring

    # Get uniV2 and uniV3 pairs
    pairs = recon.get_last_pairs()
    pairs_v3 = recon.get_last_pairs_v3()
    # print("All last pairs from UniV2:")
    # pp.pprint(pairs)
    # print("All last pairs from UniV3:")
    # pp.pprint(pairs_v3)

    # Parse the pairs to get the non WETH addresses
    non_weth_pairs = recon.parse_pairs(pairs)
    non_weth_pairs_v3 = recon.parse_pairs(pairs_v3)
    print("All Non WETH pairs from UniV2:")
    pp.pprint(non_weth_pairs)
    print("All Non WETH pairs from UniV3:")
    pp.pprint(non_weth_pairs_v3)

    # Check the security of the non WETH pairs
    security_data_objects = recon.check_security(non_weth_pairs)
    security_data_objects_v3 = recon.check_security(non_weth_pairs_v3)
    # print("All security data:")
    # pp.pprint(security_data_objects)
    # pp.pprint(security_data_objects_v3)

    # Get the open source objects
    open_source_objects = recon.get_open_source(security_data_objects)
    open_source_objects_v3 = recon.get_open_source(security_data_objects_v3)
    # add both together for later use
    open_source_objects.extend(open_source_objects_v3)
    # print("All open source objects from UniV2:")
    # pp.pprint(open_source_objects)
    # print("All open source objects from UniV3:")
    # pp.pprint(open_source_objects_v3)

    # Check the liquidity and timestamp of the open source objects
    for token in open_source_objects:
        token_address = list(token["result"].keys())[0]
        token_data = recon.screener_by_token(token_address)
        if token_data and "pairs" in token_data and token_data["pairs"]:
            token_data_object = recon.create_token_data(token, token_data)
            pp.pprint(token_data_object)
        # pp.pprint(token_data)
        if (
            token_data
            and token_data["pairs"]
            and "pairCreatedAt" in token_data["pairs"][0]
        ):
            timestamp_ms_to_s = token_data["pairs"][0]["pairCreatedAt"] / 1000.0
            dt_object = datetime.fromtimestamp(timestamp_ms_to_s)
            now = datetime.now()
            diff = now - dt_object
            print(f"Pair created at: {dt_object}")
            if diff < timedelta(minutes=5):
                print("Pair created less than 5 minutes ago")
            else:
                print("Pair created more than 5 minutes ago")
            if token_data["pairs"][0]["liquidity"]["usd"] > 20000:
                print("PREPARE TO BUY")

    # if token_data and "pairs" in token_data and token_data["pairs"]:
    #     for security_data_object, token_data in zip(
    #         open_source_objects, token_data
    #     ):
    #         token_data_object = recon.create_token_data(
    #             security_data_object, token_data
    #         )
    #         print(token_data_object)


if __name__ == "__main__":
    main()
