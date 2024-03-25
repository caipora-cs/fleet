from web3 import Web3

# Connect to BSC mainnet
web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org'))

# Address of the ERC1967Proxy contract
proxy_address = '0x2D4e39B07117937b2CB51b8a7ab8189b50D41184'

# Define the storage slot for the implementation address
implementation_slot = '0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'

# Get the implementation address from the storage slot
def get_implementation_address():
    implementation_address = web3.eth.get_storage_at(proxy_address, implementation_slot)
    return implementation_address

def bytes_to_hex(byte_str):
    return '0x' + byte_str.hex()

implementation_address = get_implementation_address()
implementation_address_hex = bytes_to_hex(implementation_address)
print("Implementation Address:", implementation_address_hex)
