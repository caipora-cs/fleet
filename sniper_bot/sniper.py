# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
import json
import time
import datetime
import os
import requests
import pprint
from goplus.token import Token
from dotenv import load_dotenv
from sniper_bot.scripts.recon import Recon
from sniper_bot.scripts.txns import Transaction
from sniper_bot.utils.style import style

ascii = """

 ______  __       ______   ______  ______  
/\  ___\/\ \     /\  ___\ /\  ___\/\__  _\ 
\ \  __\\ \ \____\ \  __\ \ \  __\\/_/\ \/ 
 \ \_\   \ \_____\\ \_____\\ \_____\ \ \_\ 
  \/_/    \/_____/ \/_____/ \/_____/  \/_/ 

                                           
"""
class Sniper:
    """Bot Main Class"""

    def __init__(self, recon: Recon, txn: Transaction) -> None:
        self.recon = recon
        self.txn = txn
        self.welcome()

    def welcome(self): 
        print(style.CYAN + ascii + style.RESET)
        print(style.GREEN + "A full stack automated trading Sniper Bot for DEX and CEX cryptocurrency" + style.RESET)
        print(style.GREEN + "---------------------------------" + style.RESET)



def main():
    """Main function."""

if __name__ == "__main__":
    main()
