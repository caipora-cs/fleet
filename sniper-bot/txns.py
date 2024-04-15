import json
import requests
from web3 import Web3


def connect():
    """Connnect to a WebSocket or HTTP RPC endpoint to the blockchain."""
    with open("settings.json") as f:
        keys = json.load(f)
    if keys["RPC_ENDPOINT"][:2].lower() == "ws":
        w3 = Web3(Web3.WebsocketProvider(keys["RPC_ENDPOINT"]))
    else:
        w3 = Web3(Web3.HTTPProvider(keys["RPC_ENDPOINT"]))
    return w3


class EthereumAddress:
    """Class to handle Ethereum addresses type.`"""

    def __init__(self, address) -> None:
        if not Web3.is_address(address):
            raise ValueError(f"{address} is not a valid Ethereum address")
        if not Web3.is_checksum_address(address):
            raise ValueError(f"{address} is not a valid checksummed Ethereum address")
        self.address = address

    def __str__(self) -> str:
        return self.address


class Transaction:
    """Class to handle transactions. Functions to buy and sell tokens based on signals."""

    def __init__(self, token_address: EthereumAddress, quantity: int = 0) -> None:
        # Wallet or Contract address
        self.address, self.private_key = self.setup_address()
        # Token to buy or sell, already checksummed
        self.token_address = token_address
        self.quantity = quantity
        self.token_contract = self.setup_token_contract()
        self.slippage = self.setup_slippage()
        self.max_gas, self.gas_price = self.setup_gas()
        self.w3 = self.connect()
