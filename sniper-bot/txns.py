import json
from web3 import Web3 
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
            keys = json.load(f)
        w3 = Web3(Web3.HTTPProvider(keys["RPC_URL"]))
        return w3
    
    def initSettings(self):
        with open("./settings.json") as f:
            keys = json.load(f)
        self.timeout = keys["timeout"]
        self.safeGas = keys["SaveGasCost"]
    
    def setupGas(self):
        with open("./settings.json") as f:
            keys = json.load(f)
        return keys['MaxTXFeeBNB'], int(keys['GWEI_GAS'] * (10**9))
    
    def setup_address(self):
        with open("./settings.json") as f:
            keys = json.load(f)
        if len(keys["metamask_address"]) <= 41:
            print(style.RED + "Set your Address in the keys.json file!" + style.RESET)
            raise SystemExit
        if len(keys["metamask_private_key"]) <= 42:
            print(style.RED + "Set your PrivateKey in the keys.json file!" + style.RESET)
            raise SystemExit
        return keys["metamask_address"], keys["metamask_private_key"]
    
    def setupSlippage(self):
        with open("./settings.json") as f:
            keys = json.load(f)
        return keys['Slippage']
    
    def get_token_decimals(self):
        return self.token_contract.functions.decimals().call()
    
    def get_token_Name(self):
        return self.token_contract.functions.name().call()

    def get_token_Symbol(self):
        return self.token_contract.functions.symbol().call()
    
    def getBlockHigh(self):
        return self.w3.eth.block_number
    
    def setup_swapper(self):
        swapper_address = Web3.to_checksum_address("0x2D4e39B07117937b2CB51b8a7ab8189b50D41184")
        with open("./abis/BSC_Swapper.json") as f:
            contract_abi = json.load(f)
        swapper = self.w3.eth.contract(address=swapper_address, abi=contract_abi)
        return swapper_address, swapper