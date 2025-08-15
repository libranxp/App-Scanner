def calculate_risk(entry_price, atr, risk_percent=1, account_size=10000):
    """
    Calculates stop loss, take profit, and position size based on ATR.
    """
    dollar_risk = account_size * (risk_percent / 100)
    stop_loss = entry_price - atr
    position_size = dollar_risk / (entry_price - stop_loss)
    take_profit = entry_price + (2 * atr)
    return {
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "position_size": int(position_size)
    }
