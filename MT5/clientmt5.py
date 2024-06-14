# clientmt5.py

import os

import MetaTrader5 as mt5
from dotenv import load_dotenv

load_dotenv()

login = int(os.getenv("MT5_ACCOUNT"))  # Convert account number to int
password = os.getenv("MT5_PASSWORD")
server = os.getenv("MT5_SERVER")


def initialize_mt5():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # Debug: Ensure that login, password, and server are correctly loaded
    if not login or not password or not server:
        print("Missing MT5 credentials. Please check your .env file.")
        quit()
    if not mt5.login(login, password, server):
        print("login() failed, error code =", mt5.last_error())
        mt5.shutdown()
        quit()
    print("Connected to MT5")


def account_info():
    account_info_dict = mt5.account_info().as_dict()
    print(account_info_dict)


def shutdown_mt5():
    mt5.shutdown()
    print("MT5 connection shut down")
