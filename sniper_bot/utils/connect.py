import json
import os
from web3 import Web3

# Get the dir of this file
dir_path = os.path.dirname(os.path.realpath(__file__))


# UniswapV2 factory address and its respective ABI
factory_address = "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"
with open(os.path.join(dir_path, "../abis/uniswapV2.abi.json"), encoding="utf-8") as f:
    factory_abi = json.load(f)

factory_address_v3 = "0x33128a8fC17869897dcE68Ed026d694621f6FDfD"
with open(os.path.join(dir_path, "../abis/uniswapV3.abi.json"), encoding="utf-8") as f:
    factory_abi_v3 = json.load(f)
# Uniswap router address and its respective ABI
weth_address = "0x4200000000000000000000000000000000000006"
router_address = "0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"
with open(
    os.path.join(dir_path, "../abis/unirouterV2.abi.json"), encoding="utf-8"
) as f:
    router_abi = json.load(f)


def connect():
    """Connnect to a WebSocket or HTTP RPC endpoint to the blockchain."""
    with open(os.path.join(dir_path, "../settings.json"), encoding="utf-8") as f:
        keys = json.load(f)
    if keys["RPC_ENDPOINT"][:2].lower() == "ws":
        w3 = Web3(Web3.WebsocketProvider(keys["RPC_ENDPOINT"]))
    else:
        w3 = Web3(Web3.HTTPProvider(keys["RPC_ENDPOINT"]))
    return w3
