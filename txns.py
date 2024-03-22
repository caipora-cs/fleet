from web3 import Web3, constants
import json
import time
# from style import style

class TXN():
    def __init__(self, token_address, quantity): 
        self.w3 = self.connect()
        self.address, self.private_key = self.setup_address()
        self.token_address = Web3.to_checksum_address(token_address)
        self.token_contract = self.setup_token()
        self.swapper_address, self.swapper = self.setup_swapper()
        self.slippage = self.setupSlippage()
        self.quantity = quantity
        self.MaxGasInETH, self.gas_price = self.setupGas()
        self.initSettings()
    
    def connect(self):
        with open("./settings.json") as f:
            data = json.load(f)
        w3 = Web3