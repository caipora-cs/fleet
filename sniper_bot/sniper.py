# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import pprint
import argparse
from dotenv import load_dotenv
from sniper_bot.scripts.recon import Recon
from sniper_bot.scripts.txns import Transaction
from sniper_bot.utils.style import style
from sniper_bot.utils.connect import (
    factory_address,
    factory_abi,
    factory_address_v3,
    factory_abi_v3,
)

asciii = """

 ______  __       ______   ______  ______  
/\  ___\/\ \     /\  ___\ /\  ___\/\__  _\ 
\ \  __\\ \ \____\ \  __\ \ \  __\\/_/\ \/ 
 \ \_\   \ \_____\\ \_____\\ \_____\ \ \_\ 
  \/_/    \/_____/ \/_____/ \/_____/  \/_/ 

                                           
"""
# Amount set for constant as of now
parser = argparse.ArgumentParser(description="Set your token amount as: sniper.py --amount <value>")
parser.add_argument('-a','--amount', default='0', type=float, required=True, help='Amount in ETH to be traded per transaction')
args = parser.parse_args()

class Sniper:
    """Bot Main Class"""

    def __init__(self, recon: Recon, txn: Transaction) -> None:
        self.parse_args()
        self.recon = recon
        self.txn = txn
        self.welcome()

    def welcome(self): 
        """Display front end on terminal"""
        print(style.CYAN + ascii + style.RESET)
        print(style.GREEN + "A full stack automated trading Sniper Bot for DEX and CEX cryptocurrency" + style.RESET)
        print(style.GREEN + "---------------------------------" + style.RESET)
    
    def parse_args(self):
        """Parse supported arguments to run bot from a terminal command"""
        self.amount = args.amount
    
    def calculate_profit(self):
        """Calculate on sell function based on value input(BUY) and value output(SELL)"""
        raise NotImplementedError 
    
    def open_positions(self):
        """Retrieve all tokens with active bought and their status"""
        raise NotImplementedError
    
    def process_pairs(self, pairs):
        """Process pairs to be used in the bot"""
        parsed_pairs = self.recon.parse_pairs(pairs)
        security_data = self.recon.check_security(parsed_pairs)
        os_data = self.recon.get_open_source(security_data)
        return os_data

def main():
    """Main function."""
    #Instantiate Recon and Transaction classes to be used in Sniper 
    recon = Recon(factory_address)
    txn = Transaction(token_address, quantity)
    sniper = Sniper(recon, txn)

    #Utils    
    pp = pprint.PrettyPrinter(indent=4)

    #Recon 
    #---------------------------
    #Prepare Recon data
    token_pairs = recon.get_last_pairs()
    token_pairs_v3 = recon.get_last_pairs_v3()
    os_data = sniper.process_pairs(token_pairs) 
    os_data_v3 = sniper.process_pairs(token_pairs_v3) 
    os_data.extend(os_data_v3)
    

if __name__ == "__main__":
    main()
