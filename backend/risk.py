# backend/risk.py
def calculate_risk(price, ai_score, account_balance=1000):
    """
    Returns stop-loss, take-profit, and recommended position size.
    """
    risk_pct = 0.02  # risk 2% per trade
    position_size = round(account_balance * risk_pct, 2)

    # Determine SL/TP based on AI score
    if ai_score >= 7:
        sl = round(price * 0.97, 2)
        tp = round(price * 1.08, 2)
    elif ai_score <= 4:
        sl = round(price * 0.99, 2)
        tp = round(price * 1.03, 2)
    else:
        sl = round(price * 0.98, 2)
        tp = round(price * 1.05, 2)

    return sl, tp, position_size
