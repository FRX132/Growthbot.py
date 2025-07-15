# logger.py
import csv
from datetime import datetime

def log_trade(signal, target_balance, lotsize, accepted):
    with open("trade_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            signal["symbol"],
            signal["direction"],
            signal["entry"],
            signal["sl"],
            signal["tp"],
            target_balance,
            lotsize,
            "YES" if accepted else "NO"
        ])