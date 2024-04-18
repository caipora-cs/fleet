import json
import requests
import style
import time
from web3 import Web3
from recon import factory_address, factory_abi

# Uniswap router address and its respective ABI
weth_address = "0x4200000000000000000000000000000000000006"
router_address = "0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"
with open("abis/unirouterV2.abi.json", encoding="utf-8") as f:
    router_abi = json.load(f)


def connect():
    """Connnect to a WebSocket or HTTP RPC endpoint to the blockchain."""
    with open("settings.json", encoding="utf-8") as f:
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
        with open("settings.json") as f:
            keys = json.load(f)
        self.w3 = connect()
        # Wallet or Contract address
        self.factory = self.w3.eth.contract(
            address=EthereumAddress(factory_address), abi=factory_abi
        )
        self.router = self.w3.eth.contract(
            address=EthereumAddress(router_address), abi=router_abi
        )
        # Token to buy or sell, already checksummed
        self.token_exchange_address = self.factory.functions.get_exchange(
            token_address
        ).call()
        # Config
        self.token_address = token_address
        self.quantity = quantity
        # Setup logic
        self.address, self.private_key = self.setup_address()
        self.token_contract = self.setup_token_contract()
        self.max_gas, self.gas_price = self.setup_gas()
        self.timeout = keys["timeout"]
        self.safegas = keys["savegascost"]
        self.slippage = keys["slippage"]

    # Methods
    def setup_token_contract(self):
        """Set up the token contract."""
        with open("abis/erc20.abi.json", encoding="utf-8") as f:
            erc20_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.token_address, abi=erc20_abi)
        return token_contract

    def setup_gas(self):
        """Set up the gas price and a max gas you are willing to accept."""
        with open("settings.json", encoding="utf-8") as f:
            keys = json.load(f)
        return keys["max_fee_eth"], int(keys["gwei_gas"] * (10**9))

    def setup_address(self):
        """Does check validation of the address and private key."""
        with open("settings.json", encoding="utf-8") as f:
            keys = json.load(f)
        if len(keys["YOUR_ADDRESS"]) <= 41:
            print(
                style.RED
                + "Please set your address in the settings.json file."
                + style.RESET
            )
            raise ValueError("Address not set in settings.json") and SystemExit
        if len(keys["YOUR_PRIVATE_KEY"]) <= 42:
            print(
                style.RED
                + "Please set your private key in the settings.json file."
                + style.RESET
            )
            raise ValueError("Private key not set in settings.json") and SystemExit
        return keys["YOUR_ADDRESS"], keys["YOUR_PRIVATE_KEY"]

    def get_token_decimals(self):
        """Get the token decimals."""
        return self.token_contract.functions.decimals().call()

    def get_token_name(self):
        """Get the token name."""
        return self.token_contract.functions.name().call()

    def get_token_symbol(self):
        """Get the token symbol."""
        return self.token_contract.functions.symbol().call()

    def get_token_balance(self):
        return self.token_contract.functions.balance_of(self.address).call()

    def get_block_high(self):
        """Get the latest block number."""
        return self.w3.eth.block_number

    def estimate_gas(self, txn):
        """Estimate the gas for a transaction."""
        gas = self.w3.eth.estimate_gas(
            {
                "from": txn["from"],
                "to": txn["to"],
                "value": txn["value"],
                "data": txn["data"],
            }
        )
        gas = gas + (gas / 10)  # Adding 1/10 from gas to gas!
        max_gas_eth = Web3.from_wei(gas * self.gas_price, "ether")
        print(
            style.GREEN
            + "\nMax Transaction cost "
            + str(max_gas_eth)
            + "ETH"
            + style.RESET
        )
        if max_gas_eth > self.max_gas:
            print(style.RED + "\nTx cost exceeds your settings, exiting!")
            raise SystemExit  # Find better exception to raise
        return gas

    # Funcao para dar retrieve da liquidity da wallet e do token

    def get_output_token_to_eth(self, percent: int = 100):
        """Get the amount of token to be sold."""
        token_balance = int(
            self.token_contract.functions.balance_of(self.address).call()
        )
        if token_balance > 0:
            amount_for_input = int((token_balance / 100) * percent)
            if percent == 100:
                amount_for_input = token_balance
        return amount_for_input

    # Buy Logic
    def buy_token(self, retry: int = 1):
        """Buy tokens with a given amount of ETH. Retry if the transaction fails. cheap or fast"""
        if self.safegas != True:
            return self.buy_token_fast(retry)
        else:
            return self.buy_token_cheap(retry)

    def buy_token_fast(self, trys):
        while trys:
            try:
                # Get the Uniswap router  contract
                uniswap_router = self.w3.eth.contract(
                    address=router_address, abi=router_abi
                )
                # Set the deadline for 5 minutes
                deadline = int(time.time()) + 5 * 60
                # Build transaction for router
                txn = uniswap_router.functions.swapExactETHForTokens(
                    0,  # The minimum amount of token you want to receive
                    [weth_address, self.token_address],  # The path of the swap
                    self.address,  # Recipient of the output tokens
                    deadline,
                ).build_transaction(
                    {
                        "from": self.address,
                        "value": self.w3.toWei(int(self.quantity), "ether"),
                        "gasPrice": self.gas_price,
                        "nonce": self.w3.eth.get_transaction_count(self.address),
                    }
                )

                txn.update({"gas": self.estimate_gas(txn)})
                signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
                txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(style.GREEN + "Transaction sent: " + style.RESET + str(txn.hex()))
                txn_receipt = self.w3.eth.wait_for_transaction_receipt(
                    txn, timeout=self.timeout
                )
                if txn_receipt["status"] == 1:
                    return True, print(
                        style.GREEN + "Transaction successful!" + style.RESET
                    )
                else:
                    return False, print(style.RED + "Transaction failed!" + style.RESET)
            except Exception as e:
                print(e)
                trys -= 1
                print(style.RED + "Transaction failed, retrying..." + style.RESET)
                time.sleep(1)
