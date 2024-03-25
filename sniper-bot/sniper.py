import requests
import time
import datetime
import requests
from goplus.token import Token

BASESCAN_API_URL = "https://api.basescan.org/api"
BASESCAN_API_KEY = "8UPKW51SE8WMJDJUR1DA7D6YTDSB4MDW8N"

def is_contract_verifiable(contract_address):
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": BASESCAN_API_KEY
    }

    response = requests.get(BASESCAN_API_URL, params=params)
    data = response.json()

    return 'status' in data and data['status'] == '1' and 'result' in data and len(data['result']) > 0 and data['result'][0]['ContractName'] != ''

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

while True:
    response = requests.post(url, json={'query': query})
    data = response.json()

    if 'data' in data and 'pools' in data['data']:
        for pool in data['data']['pools']:
            timestamp = datetime.datetime.fromtimestamp(int(pool['createdAtTimestamp']))
            liquidity = float(pool['liquidity'])
            token1_address = pool['token1']['id']
            token1_security_data = Token().token_security(
                chain_id="8453", addresses=[token1_address]
            )
            if not is_contract_verifiable(token1_address):
                print(f"Warning: Token1 address {token1_address} is not verifiable")
            else:
                print(f"Token1 address {token1_address} is verifiable")
                print(f"Token1 security data: {token1_security_data}")
            print(f"Pair: {pool['token0']['symbol']}/{pool['token1']['symbol']}")
            print(f"Created at: {timestamp}")
            print(f"Liquidity: {liquidity:.2f}")
    else:
        print(f"Error: Unexpected response: {data}")

    time.sleep(60)  # wait for 60 seconds before the next request