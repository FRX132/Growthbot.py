# confirmations.py
def confirm_with_rules(price, entry, direction):
    if direction == "BUY" and price > entry:
        return True
    if direction == "SELL" and price < entry:
        return True
    return False