import random

def check_for_signal():
    # Simulierter Preisverlauf
    low = round(random.uniform(2328.00, 2333.00), 2)
    high = round(random.uniform(2335.00, 2343.00), 2)
    current_price = round(random.uniform(2330.00, 2343.00), 2)

    # Setup-Level
    entry = 2334.55
    sl = 2330.55
    tp = 2343.55

    # --- BUY SETUP ---
    if low < entry and current_price > entry:
        spread = abs(current_price - entry)
        if spread <= 2.0:
            distance_total = tp - entry
            distance_now = current_price - entry
            if distance_now >= 0.4 * distance_total:
                sl = round(entry + 0.2 * distance_total, 2)

            # Kategorisierung: Spread + Tiefe
            if low < entry - 2:
                category = "A"
            elif low < entry - 1:
                category = "B"
            else:
                category = "C"

            return {
                "symbol": "XAUUSD",
                "direction": "BUY",
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "category": category
            }

    # --- SELL SETUP ---
    entry_sell = 2334.55
    sl_sell = 2338.55
    tp_sell = 2326.55

    if high > entry_sell and current_price < entry_sell:
        spread = abs(current_price - entry_sell)
        if spread <= 2.0:
            distance_total = entry_sell - tp_sell
            distance_now = entry_sell - current_price
            if distance_now >= 0.4 * distance_total:
                sl_sell = round(entry_sell - 0.2 * distance_total, 2)

            if high > entry_sell + 2:
                category = "A"
            elif high > entry_sell + 1:
                category = "B"
            else:
                category = "C"

            return {
                "symbol": "XAUUSD",
                "direction": "SELL",
                "entry": entry_sell,
                "sl": sl_sell,
                "tp": tp_sell,
                "category": category
            }

    return None