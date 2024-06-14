import MetaTrader5 as mt5
from flask import Flask, jsonify, request

import Utils.utils as ut
from MT5.clientmt5 import initialize_mt5, shutdown_mt5
from MT5.live_data import get_latest_candles
from Trade.trade import execute_bias_order, get_entry

app = Flask(__name__)


@app.route("/")
def unauthorised():
    app.status = 401
    return "You are not authorised to view this page"


@app.route("/ping")
def pong():
    app.status = 200
    return "pong"


@app.route("/candles/<symbol>/<timeframe>/<count>")
def get_candles(symbol, timeframe, count):
    try:
        count = int(count)
        timeframe = getattr(mt5, f"TIMEFRAME_{timeframe.upper()}")
        candles = get_latest_candles(symbol, timeframe, count)
        return jsonify(candles.tolist())
    except Exception as e:
        return str(e), 400


@app.route("/get_best_entry", methods=["POST"])
def get_best_entry():
    try:
        data = request.json
        bias = data.get("bias")
        overrideCheck = data.get("overrideCheck")
        symbol = data.get("symbol")
        timeframe = data.get("timeframe")
        count = data.get("count")
        if None in [bias, overrideCheck, symbol, timeframe, count]:
            return "Missing parameters", 400
        # Convert overrideCheck to a boolean
        if isinstance(overrideCheck, str):
            overrideCheck = overrideCheck.lower() in ["true", "1", "t", "y", "yes"]
        else:
            overrideCheck = bool(overrideCheck)

        count = int(count)
        timeframe = getattr(mt5, f"TIMEFRAME_{timeframe.upper()}")
        best_entry = get_entry(bias, overrideCheck, symbol, timeframe, count)
        if best_entry != None:
            return jsonify(best_entry), 200
        else:
            return "No entry found", 404
    except ut.TradeWindowError as e:
        print(f"Trade window error: {e}")
        return "Trade window error", 400
    except ut.InsufficientDataError as e:
        print(f"Insufficient data error: {e}")
        return "Insufficient data", 400
    except ut.ConditionNotMetError as e:
        print(f"Condition not met error: {e}")
        return "Condition not met", 400
    except ut.InvalidBiasError as e:
        print(f"Invalid bias error: {e}")
        return "Bias must be 'sell' or 'buy'", 400
    except ut.TradeWindowBreach as e:
        print(f"Trade window breach error: {e}")
        return "Trade window breach", 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


@app.route("/place_precise_order", methods=["POST"])
def place_precise_order():
    try:
        data = request.json
        bias = data.get("bias")
        overrideCheck = data.get("overrideCheck")
        symbol = data.get("symbol")
        timeframe = data.get("timeframe")
        count = data.get("count")
        volume = data.get("volume")
        if None in [bias, overrideCheck, symbol, timeframe, count, volume]:
            return "Missing parameters", 400
        # Convert overrideCheck to a boolean
        if isinstance(overrideCheck, str):
            overrideCheck = overrideCheck.lower() in ["true", "1", "t", "y", "yes"]
        else:
            overrideCheck = bool(overrideCheck)

        count = int(count)
        volume = float(volume)
        timeframe = getattr(mt5, f"TIMEFRAME_{timeframe.upper()}")

        order = execute_bias_order(
            bias,
            overrideCheck,
            symbol,
            timeframe,
            count,
            volume,
        )
        if order != None:
            return jsonify(order), 200
        else:
            return "No entry found", 404
    except ut.TradeWindowError as e:
        print(f"Trade window error: {e}")
        return "Trade window error", 400
    except ut.InsufficientDataError as e:
        print(f"Insufficient data error: {e}")
        return "Insufficient data", 400
    except ut.ConditionNotMetError as e:
        print(f"Condition not met error: {e}")
        return "Condition not met", 400
    except ut.InvalidBiasError as e:
        print(f"Invalid bias error: {e}")
        return "Bias must be 'sell' or 'buy'", 400
    except ut.TradeWindowBreach as e:
        print(f"Trade window breach error: {e}")
        return "Trade window breach", 400
    except ut.ErrorPlacingOrder as e:
        print(f"Error placing order: {e}")
        return "Error placing order", 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    initialize_mt5()
    try:
        app.run(debug=True, host="0.0.0.0", port=503)
    except KeyboardInterrupt:
        # Ensure MT5 is properly shut down when the server stops
        shutdown_mt5()
