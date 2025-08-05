# mt5_feed.py
import MetaTrader5 as mt5

def connect_mt5():
    if not mt5.initialize():
        raise Exception("❌ MetaTrader 5 konnte nicht initialisiert werden")
    print("✅ Verbindung zu MT5 erfolgreich")

def get_price(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise Exception(f"❌ Kein Tick-Daten für {symbol} verfügbar")
    
    return {
    "bid": tick.bid,
    "ask": tick.ask,
    "time": tick.time
}
    
def shutdown_mt5():
    mt5.shutdown()