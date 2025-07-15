# mt5_feed.py
import MetaTrader5 as mt5

def connect_mt5():
    if not mt5.initialize():
        print("MT5 init failed")
        return False
    return True

def get_price(symbol):
    tick = mt5.symbol_info_tick(symbol)
    return tick.ask if tick else None