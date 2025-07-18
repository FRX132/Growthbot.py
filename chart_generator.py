import matplotlib.pyplot as plt
import os

def generate_chart(symbol, entry, sl, tp, direction, current_price, category):
    plt.figure(figsize=(6, 4))
    prices = [sl, entry, tp]
    labels = ["SL", "Entry", "TP"]

    # Farben
    color = "green" if direction == "BUY" else "red"
    
    for level, label in zip(prices, labels):
        plt.axhline(y=level, color=color, linestyle="--", label=label)

    plt.axhline(y=current_price, color="blue", linestyle="-", label="Current Price")
    plt.title(f"{symbol} {direction} Signal ({category})")
    plt.legend()
    plt.xlabel("Zeit (simuliert)")
    plt.ylabel("Preis")
    plt.grid(True)

    filename = "trade_signal_chart.png"
    plt.savefig(filename)
    plt.close()
    return filename