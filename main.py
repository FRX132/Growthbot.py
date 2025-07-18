from logger import log_trade
from mt5_feed import connect_mt5, get_price
from confirmations import confirm_with_rules
from signal_logic import check_for_signal
from notifier import send_telegram_alert
from growth_model import calc_target_balance, calc_lot_size
import time
from chart_generator import generate_chart
from datetime import datetime

x = 0  # Trade-Zähler
start_balance = 100
growth_rate = 1.05
risk_percent = 3.0
sl_usd = 3.0

def main_loop():
    global x
    while x < 200:
        signal = check_for_signal()
        # Session-Zeitprüfung (UTC+2)
        def is_in_session(symbol):
            now = datetime.now()
            current_minutes = now.hour * 60 + now.minute

            if symbol in ["XAUUSD", "BTCUSD"]:
                return (14*60 <= current_minutes <= 16*60) or (2*60 <= current_minutes <= 4*60)
            elif symbol in ["GBPJPY", "EURUSD"]:
                return 6*60 <= current_minutes <= 8*60
            elif symbol == "USDJPY":
                return (23*60 <= current_minutes <= 24*60) or (0 <= current_minutes <= 1*60)
            return False

        if not signal or not is_in_session(signal['symbol']):
            print(f"⏱ Kein gültiger Session-Zeitraum für {signal['symbol']} – übersprungen")
            time.sleep(60)
            continue

        target_balance = calc_target_balance(start_balance, growth_rate, x)
        lotsize = calc_lot_size(target_balance, risk_percent, sl_usd)
        msg = f"""🚨 Trade #{x + 1}
Symbol: {signal['symbol']}
Richtung: {signal['direction']}
Entry: {signal['entry']}
SL: {signal['sl']}
TP: {signal['tp']}
📈 Zielkapital: {target_balance} €
📦 Lotgröße bei 1% Risiko: {lotsize} Lot
"""
        image_path = generate_chart(
            signal["symbol"],
            signal["entry"],
            signal["sl"],
            signal["tp"],
            signal["direction"],
            get_price(signal["symbol"]),
            signal["category"]
        )

        send_telegram_alert(msg, image_path)
        x += 1

        # init MT5 und Preis abrufen
        connect_mt5()
        live_price = get_price(signal["symbol"])
        if not confirm_with_rules(live_price, signal["entry"], signal["direction"]):
            print("⚠️ Setup nicht bestätigt durch Live-Daten")
            continue

        user_input = input("Signal umsetzen? (j/n): ").lower()
        accepted = user_input == "j"
        log_trade(signal, target_balance, lotsize, accepted)

        if accepted:
            print(">> Signal angenommen (kann später mit Bot oder manuell ausgeführt werden)")
        else:
            print(">> Signal abgelehnt")
        time.sleep(60)



if __name__ == "__main__":
    main_loop()