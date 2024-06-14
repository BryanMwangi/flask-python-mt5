import MetaTrader5 as mt5

import MT5.live_data as ld
import Trade.timecheck as tc
import Utils.utils as ut


def place_order(symbol, volume, order_type, price, sl, tp, magic):
    """
    Place an order on the MT5 platform.

    Args:
        symbol (str): The trading symbol (e.g., 'EURUSD').
        volume (float): The volume of the trade.
        order_type (int): The type of order (e.g., mt5.ORDER_TYPE_BUY or mt5.ORDER_TYPE_SELL).
        price (float): The price at which to place the order.
        sl (float, optional): The stop-loss price.
        tp (float, optional): The take-profit price.

    Returns:
        dict: The result of the order placement.
    """
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": 20,
        "sl": sl,
        "tp": tp,
        "magic": magic,
        "comment": "Python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise ut.ErrorPlacingOrder(f"Order send failed, retcode = {result.retcode}")

    return result._asdict()


def get_entry(bias, overrideCheck, symbol, timeframe, count):
    """
    we try and get the right position to enter the market based on bias of analyst
    """
    if bias == "sell" or bias == "buy":
        if overrideCheck != True:
            can_trade = tc.check_trade_window()
            if not can_trade:
                raise ut.TradeWindowError(
                    "Trade window check failed. You are not allowed to trade at this time"
                )

            print("trade window check passed")

            # check last 3 candles open, high, low and close rates to determine right point of entry
            candles = ld.get_latest_candles(symbol, timeframe, count)
            if len(candles) < 3:
                print("Not enough candles to analyze")
                raise ut.InsufficientDataError("Not enough candles to analyze")
            # Extract the candles
            third_last_candle = candles[-3]
            second_last_candle = candles[-2]

            if bias == "sell":
                # Check if the high of the second last candle is higher than the open or low of the third last candle
                if (
                    second_last_candle["high"] > third_last_candle["open"]
                    or second_last_candle["high"] > third_last_candle["low"]
                ):
                    # Determine the right entry point
                    entry_point = (
                        second_last_candle["high"]
                        + (second_last_candle["high"] - second_last_candle["low"]) * 0.1
                    )  # example calculation
                    print(f"Recommended entry point for sell: {entry_point}")
                    return entry_point
                else:
                    print("Condition for entry not met")
                    return None
            if bias == "buy":
                # Check if the high of the second last candle is higher than the open or low of the third last candle
                if (
                    second_last_candle["low"] > third_last_candle["open"]
                    or second_last_candle["open"] < third_last_candle["low"]
                ):
                    # Determine the right entry point
                    entry_point = (
                        second_last_candle["high"]
                        - (second_last_candle["high"] + second_last_candle["low"]) * 0.1
                    )  # example calculation
                    print(f"Recommended entry point for buy: {entry_point}")
                    return entry_point
                else:
                    print("Condition for entry not met")
                    return None
        else:
            raise ut.TradeWindowBreach(
                "You are trying to make a trade with an invalid window"
            )
    else:
        raise ut.InvalidBiasError("Bias must be 'sell' or 'buy'")


def execute_bias_order(
    bias,  # sell or buy
    overrideCheck,  # true or false
    symbol,  # symbol for trade eg. XAUUSD
    timeframe,  # timeframe (int): The timeframe for the candles (e.g., mt5.TIMEFRAME_M1).
    count,  # count (int): The number of candles to retrieve.
    volume,  # (float): The volume of the trade
):
    """
    execute the bias order
    """
    # get the entry point
    price = get_entry(bias, overrideCheck, symbol, timeframe, count)
    if price != None:
        # Calculate lot size, SL, and TP
        pip_value = mt5.symbol_info(symbol).point  # Example for most forex pairs
        print(f"pip_value:{pip_value}")
        if "XAU" in symbol:
            scale_factor = 1000
        else:
            scale_factor = 100
        if bias == "sell":
            sl = price + (scale_factor * pip_value)
            tp = price - (scale_factor * pip_value * 2)
            order_type = mt5.ORDER_TYPE_SELL_LIMIT
            magic = 22343

        if bias == "buy":
            sl = price - (scale_factor * pip_value)
            tp = price + (scale_factor * pip_value * 2)
            order_type = mt5.ORDER_TYPE_BUY_LIMIT
            magic = 22353

        print(
            f"price:{price},sl:{sl}, tp:{tp}, order_type:{bias}, magic:{magic}, symbol:{symbol}, volume:{volume}"
        )
        order = place_order(symbol, volume, order_type, price, sl, tp, magic)
        print(order)
        return order
    else:
        return None
