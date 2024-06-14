import datetime
from zoneinfo import ZoneInfo

import MetaTrader5 as mt5

acceptable_trade_windows = {
    "NY_Morning": ("09:00", "13:00"),  # change back to 11:00
    "LN_Morning": ("20:00", "22:00"),
    "HK_Morning": ("02:00", "05:00"),
}


timeframes_mapping = {
    "1-minute": [mt5.TIMEFRAME_M1, 1],
    "2-minutes": [mt5.TIMEFRAME_M2, 2],
    "3-minutes": [mt5.TIMEFRAME_M3, 3],
    "4-minutes": [mt5.TIMEFRAME_M4, 4],
    "5-minutes": [mt5.TIMEFRAME_M5, 5],
    "6-minutes": [mt5.TIMEFRAME_M6, 6],
    "10-minutes": [mt5.TIMEFRAME_M10, 10],
    "12-minutes": [mt5.TIMEFRAME_M12, 12],
    "15-minutes": [mt5.TIMEFRAME_M15, 15],
    "30-minutes": [mt5.TIMEFRAME_M30, 30],
    "1-hour": [mt5.TIMEFRAME_H1, 60],
    "2-hours": [mt5.TIMEFRAME_H2, 120],
    "3-hours": [mt5.TIMEFRAME_H3, 180],
    "4-hours": [mt5.TIMEFRAME_H4, 240],
    "6-hours": [mt5.TIMEFRAME_H6, 360],
    "8-hours": [mt5.TIMEFRAME_H8, 420],
    "12-hours": [mt5.TIMEFRAME_H12, 720],
    "1-day": [mt5.TIMEFRAME_D1, 1440],
}


def check_trade_window():
    """
    Check if the current time is within the trade window.

    Returns:
        bool: True if the time is within the trade window, False otherwise.
    """
    current_time = datetime.datetime.now(ZoneInfo("America/New_York")).time()

    for window, time_range in acceptable_trade_windows.items():
        start_time = datetime.time.fromisoformat(time_range[0])
        end_time = datetime.time.fromisoformat(time_range[1])
        if start_time <= current_time <= end_time:
            return True
    return False
