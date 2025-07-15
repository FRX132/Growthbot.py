from logger import log_trade
from mt5_feed import connect_mt5, get_price
from confirmations import confirm_with_rules
from signal_logic import check_for_signal
from notifier import send_telegram_alert
from growth_model import calc_target_balance, calc_lot_size
import time

x = 0  # Trade-Zähler
start_balance = 100
growth_rate = 1.05
risk_percent = 3.0
sl_EUR = 3.0

def main_loop():
    global x
    while x < 200:
        signal = check_for_signal()
        if signal:
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
    send_telegram_alert(msg)
            x += 1
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
# init MT5
connect_mt5()

# innerhalb der Schleife nach send_telegram_alert(msg)
user_input = input("Signal umsetzen? (j/n): ").lower()
accepted = user_input == "j"

# loggen
log_trade(signal, target_balance, lotsize, accepted)

if accepted:
    print(">> Signal angenommen (kann später mit Bot oder manuell ausgeführt werden)")
else:
    print(">> Signal abgelehnt")
    

live_price = get_price(signal["symbol"])
if not confirm_with_rules(live_price, signal["entry"], signal["direction"]):
    print("⚠️ Setup nicht bestätigt durch Live-Daten")
    return