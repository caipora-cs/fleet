# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import time
import datetime
import os
import requests
from goplus.token import Token
from dotenv import load_dotenv
from recon import Recon

# Load environment variables from .env file for API blockchain scan acess
load_dotenv()
SCAN_API_URL = os.getenv("BASESCAN_API_URL")
SCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
# Configure the Graph API URL and query
url = "https://gateway-arbitrum.network.thegraph.com/api/329a723890246b9fac8f970aa2ef9425/subgraphs/id/HMuAwufqZ1YCRmzL2SfHTVkzZovC9VL2UAKhjvRqKiR1"
query = """
{
    pools(first: 10, where: {token0: "0x4200000000000000000000000000000000000006"}, orderBy: createdAtTimestamp, orderDirection: desc) {
        id
        token0 {
            id
            symbol
        }
        token1 {
            id
            symbol
        }
        createdAtTimestamp
        liquidity
    }
}
"""
FACTORY_ADDRESS = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"


class Sniper:
    """Bot Main Class"""

    def __init__(self, api_url: str, api_key: str) -> None:
        self.api_url = api_url
        self.api_key = api_key

    def is_contract_verifiable(self, contract_address: str):
        """Check if a contract is verifiable on the blockchain scan API."""
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address,
            "apikey": self.api_key,
        }

        response = requests.get(self.api_url, params=params, timeout=10)
        data = response.json()

        return (
            "status" in data
            and data["status"] == "1"
            and "result" in data
            and len(data["result"]) > 0
            and data["result"][0]["ContractName"] != ""
        )

    def query_data(self, _query: str) -> dict:
        """Query data from the Graph."""
        response = requests.post(url, json={"query": query}, timeout=10)
        return response.json()
        # Add other methods here...


def main():
    """Main function."""
    sniper = Sniper(SCAN_API_URL, SCAN_API_KEY)
    recon = Recon(FACTORY_ADDRESS)
    while True:
        try:
            data_univ3 = sniper.query_data(query)
            # recon.run()

            # Check for pools datapoints and verify the contract through Scan
            # and Goplus and print for the user.
            if "data" in data_univ3 and "pools" in data_univ3["data"]:
                for pool in data_univ3["data"]["pools"]:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(pool["createdAtTimestamp"])
                    )
                    liquidity = float(pool["liquidity"])
                    token1_address = pool["token1"]["id"]
                    token1_security_data = Token().token_security(
                        chain_id="8453", addresses=[token1_address]
                    )
                    # Pools data for user
                    print("UniV3\n")
                    print(
                        f"Pair: {pool['token0']['symbol']}/{pool['token1']['symbol']}"
                    )
                    print(f"Created at: {timestamp}")
                    print(f"Liquidity: {liquidity:.2f}")
                    # Verify the contract and Check for security data
                    if not sniper.is_contract_verifiable(token1_address):
                        print(
                            f"Warning: Token1 address {token1_address} is not verifiable\n\n"
                        )
                    else:
                        print(f"Token1 address {token1_address} is verifiable")
                        print(f"Token1 security data: {token1_security_data}\n\n")

        except requests.exceptions.RequestException as error:
            print(f"Error: Unexpected response: {error}")
        time.sleep(60)
        recon.run()


if __name__ == "__main__":
    main()
