# pylint: disable=invalid-name
import json
import time
import os
from sniper_bot.utils.style import style
from web3 import Web3
from web3.exceptions import TimeExhausted, TransactionNotFound
from sniper_bot.utils.connect import (
    factory_address,
    factory_abi,
    router_address,
    router_abi,
    weth_address,
    connect,
)


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
    """Class to handle transactions. Functions to buy and sell tokens based on signals.
    Parameters:
    token_address: A Ethereum validated address
    quantity: Quantitiy in ETH
    """

    def __init__(self, token_address: EthereumAddress, quantity: float = 0) -> None:
        with open("settings.json", encoding="utf-8") as f:
            keys = json.load(f)
        self.w3 = connect()
        # Wallet or Contract address
        self.factory = self.w3.eth.contract(
            address=str(EthereumAddress(factory_address)), abi=factory_abi
        )
        self.router = self.w3.eth.contract(
            address=str(EthereumAddress(router_address)), abi=router_abi
        )
        # Token to buy or sell, already checksummed
        self.token_exchange_address = self.factory.functions.getPair(
            str(token_address), weth_address
        ).call()
        # Config
        self.token_address = str(token_address)
        self.quantity = quantity
        # Setup logic
        self.address, self.private_key = self.setup_address()
        self.token_contract = self.setup_token_contract()
        self.max_gas, self.gas_price = self.setup_gas()
        self.timeout = keys["timeout"]
        self.safegas = keys["savegascost"]
        self.slippage = keys["slippage"]
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    # Methods
    def setup_token_contract(self):
        """Set up the token contract."""
        with open(
            os.path.join(self.dir_path, "../abis/erc20.abi.json"), encoding="utf-8"
        ) as f:
            erc20_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.token_address, abi=erc20_abi)
        return token_contract

    def setup_gas(self):
        """Set up the gas price and a max gas you are willing to accept."""
        with open(
            os.path.join(self.dir_path, "../settings.json"), encoding="utf-8"
        ) as f:
            keys = json.load(f)
        gas_price = self.w3.eth.gas_price
        return keys["max_fee_eth"], gas_price

    def setup_address(self):
        """Does check validation of the address and private key."""
        with open(
            os.path.join(self.dir_path, "../settings.json"), encoding="utf-8"
        ) as f:
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
        return self.token_contract.functions.balanceOf(self.address).call()

    def get_block_high(self):
        """Get the latest block number."""
        return self.w3.eth.block_number

    def estimate_gas(self, txn):
        """Estimate the gas for a transaction."""
        estimated_gas = self.w3.eth.estimate_gas(
            {
                "from": txn["from"],
                "to": txn["to"],
                "value": txn["value"],
                "data": txn["data"],
            }
        )
        # Get the current base fee from the network
        latest_block = self.w3.eth.get_block("latest")
        base_fee = latest_block["baseFeePerGas"]
        # Set max fee per gas to be 10% higher than the base fee
        max_fee_per_gas = base_fee * 1.5
        # Calculate the total cost of the transaction
        total_cost = estimated_gas * max_fee_per_gas
        # Convert to ether
        total_cost_eth = Web3.from_wei(total_cost, "ether")
        print(
            style.GREEN
            + "\nEstimated transaction cost: "
            + str(total_cost_eth)
            + " ETH"
            + style.RESET
        )
        # Check if the total cost exceeds the maximum allowed cost
        if total_cost_eth > self.max_gas:
            print(style.RED + "\nTransaction cost exceeds your settings, exiting!")
            raise SystemExit  # Find better exception to raise
        return estimated_gas, max_fee_per_gas

    # Funcao para dar retrieve da liquidity da wallet e do token

    def get_output_token_to_eth(self, percent: int = 100):
        """Get the amount of token to be sold."""
        amount_for_input = 0
        token_balance = int(
            self.token_contract.functions.balanceOf(self.address).call()
        )
        if token_balance > 0:
            amount_for_input = int((token_balance / 100) * percent)
            if percent == 100:
                amount_for_input = token_balance
        return amount_for_input

    # Buy Logic
    def buy_token(self, retry: int = 1):
        """Buy tokens with a given amount of ETH. Retry if the transaction fails. cheap or fast"""
        if self.safegas is not True:
            return self.buy_token_fast(retry)
        else:
            return NotImplementedError(
                "The method buy_token_cheap needs to be implemented"
            )
        #   return self.buy_token_cheap(retry)

    def buy_token_fast(self, trys):
        """Buy tokens with a given amount of ETH. Retry if the transaction fails. Main logic of buy feature. """
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
                        "value": self.w3.to_wei(self.quantity, "ether"),
                        "nonce": self.w3.eth.get_transaction_count(self.address),
                    }
                )
                gas, max_fee = self.estimate_gas(txn)
                txn.update(
                    {
                        "gas": gas,
                        "maxFeePerGas": int(max_fee),
                        "maxPriorityFeePerGas": int(max_fee * 0.5),
                    }
                )
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

            except ValueError as e:
                print(style.RED + "Value Error: " + str(e) + style.RESET)
                break

            except TransactionNotFound as e:
                print(style.RED + "Transaction not found: " + str(e) + style.RESET)
                trys -= 1

            except TimeExhausted as e:
                print(style.RED + "Transaction timed out: " + str(e) + style.RESET)
                trys -= 1

            except Exception as e:
                print(style.RED + "Unexpected error:" + str(e) + style.RESET)
                trys -= 1

            time.sleep(1)

    def approve_uniswap_router(self, amount):
        """Approve the Uniswap router to transfer tokens from your address."""
        token_contract = self.token_contract
        txn = token_contract.functions.approve(
            router_address, amount
        ).build_transaction(
            {
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
            }
        )
        gas, max_fee = self.estimate_gas(txn)
        txn.update(
            {
                "gas": gas,
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_fee * 0.5),
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash

    def wait_for_transaction_receipt(self, txn_hash, timeout=300):
        """Wait for a transaction to be mined and return the transaction receipt."""
        start_time = time.time()
        while True:
            try:
                txn_receipt = self.w3.eth.get_transaction_receipt(txn_hash)
                if txn_receipt is not None:
                    return txn_receipt
            except TransactionNotFound:
                # If the transaction is not found, wait for a second and try again
                time.sleep(1)
            if time.time() - start_time > timeout:
                # If the timeout is reached, raise an exception
                raise TimeoutError(
                    f"Transaction {txn_hash} not found after {timeout} seconds"
                )

    def check_allowance(self, spender, amount):
        """Check if the spender has enough allowance."""
        token_contract = self.token_contract
        allowance = token_contract.functions.allowance(self.address, spender).call()
        return allowance >= amount

    def sell_tokens(self, percent: int = 100):
        """Sell tokens with a given amount of ETH."""
        token_balance = self.get_output_token_to_eth(percent)
        if token_balance > 0:
            amount_for_sell = int((token_balance / 100) * percent)
            if percent == 100:
                amount_for_sell = token_balance
            if self.safegas is not True:
                return self.sell_tokens_fast(amount_for_sell)
            else:
                raise NotImplementedError(
                    "The method sell_tokens_cheap needs to be implemented"
                )
        #                return self.sell_tokens_cheap(amount_for_sell)
        else:
            print(style.RED + "No tokens to sell!" + style.RESET)

    def sell_tokens_fast(self, amount: float):
        """Sell tokens with a given amount of ETH. Main logic of sell feature."""
        try:
            uniswap_router = self.w3.eth.contract(
                address=router_address, abi=router_abi
            )
            deadline = int(time.time()) + 5 * 60
            txn = uniswap_router.functions.swapExactTokensForETH(
                amount,
                0,
                [self.token_address, weth_address],
                self.address,
                deadline,
            ).build_transaction(
                {
                    "from": self.address,
                    "value": 0,
                    "nonce": self.w3.eth.get_transaction_count(self.address),
                }
            )
            gas, max_fee = self.estimate_gas(txn)
            txn.update(
                {
                    "gas": gas,
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_fee * 0.5),
                }
            )
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

        except ValueError as e:
            print(style.RED + "Value Error: " + str(e) + style.RESET)

        except TransactionNotFound as e:
            print(style.RED + "Transaction not found: " + str(e) + style.RESET)

        except TimeExhausted as e:
            print(style.RED + "Transaction timed out: " + str(e) + style.RESET)

        except Exception as e:
            print(style.RED + "Unexpected error:" + str(e) + style.RESET)

    time.sleep(1)


def main():
    """Main function."""
    print("Welcome to the Uniswap bot!")
    print("Please enter the token address you want to buy:")
    token_address = input()
    print("Please enter the amount of ETH you want to spend:")
    quantity = float(input())
    token = token_address
    transaction = Transaction(token, quantity)
    print("Token name: " + transaction.get_token_name())
    print("Token symbol: " + transaction.get_token_symbol())
    print("Token decimals: " + str(transaction.get_token_decimals()))
    print("Token balance: " + str(transaction.get_token_balance()))
    print("Block high: " + str(transaction.get_block_high()))
    print("Output token to ETH: " + str(transaction.get_output_token_to_eth()))
    print("Buying token...")
    transaction.buy_token()
    print("Aproving token for sell...")
    if not transaction.check_allowance(
        router_address, transaction.get_output_token_to_eth()
    ):
        transaction.wait_for_transaction_receipt(
            transaction.approve_uniswap_router(transaction.get_output_token_to_eth())
        )
        print("Selling token...")
    transaction.sell_tokens()
    print("Done!")


if __name__ == "__main__":
    main()
