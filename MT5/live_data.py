from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd

pd.set_option("display.max_columns", 500)  # number of columns to be displayed
pd.set_option("display.width", 1500)  # max table width to display


def get_latest_candles(symbol, timeframe, count):
    """
    Retrieve the latest candles for a given symbol, timeframe, and count.

    Args:
        symbol (str): The trading symbol (e.g., 'EURUSD').
        timeframe (int): The timeframe for the candles (e.g., mt5.TIMEFRAME_M1).
        count (int): The number of candles to retrieve.

    Returns:
        list: A list of candles.
    """
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None:
        raise RuntimeError(f"Failed to get rates, error code = {mt5.last_error()}")
    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the datetime format
    rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")
    # display data
    print("\nDisplay requested data:")
    print(rates_frame)

    return rates


def get_current_price(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Failed to get tick for {symbol}, error code =", mt5.last_error())
        return None
    return tick
