# executor.py
import MetaTrader5 as mt5

def execute_trade(signal):
    if not mt5.initialize():
        raise Exception("❌ MT5 konnte nicht initialisiert werden")

    if not mt5.symbol_select(signal["symbol"], True):
        raise Exception(f"❌ Symbol {signal['symbol']} konnte nicht aktiviert werden")

    tick = mt5.symbol_info_tick(signal["symbol"])
    if tick is None:
        raise Exception(f"❌ Keine Tick-Daten für {signal['symbol']}")

    action = mt5.ORDER_TYPE_BUY if signal["direction"].upper() == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if action == mt5.ORDER_TYPE_BUY else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": signal["symbol"],
        "volume": float(signal["lotsize"]),
        "type": action,
        "price": price,
        "sl": float(signal["sl"]),
        "tp": float(signal["tp"]),
        "deviation": 10,
        "magic": 234000,
        "comment": f"TelegramSignal {signal.get('category', '')}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"❌ Trade-Fehler: {result.comment}")
    
    print(f"✅ Trade erfolgreich ausgeführt: {signal['symbol']} {signal['direction']} @ {price}")