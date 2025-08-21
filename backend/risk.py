def calculate_risk_profile(price, atr, confidence, capital=1000):
    """
    price: current asset price
    atr: average true range (volatility proxy)
    confidence: 'High', 'Medium', or 'Low'
    capital: total capital allocated per trade
    """

    # Risk multiplier based on confidence
    risk_map = {
        "High": 1.5,
        "Medium": 1.0,
        "Low": 0.5
    }

    multiplier = risk_map.get(confidence, 1.0)

    # Stop-loss and take-profit levels
    stop_loss = round(price - atr * multiplier, 2)
    take_profit = round(price + atr * multiplier * 2.5, 2)

    # Position sizing (risking 2% of capital)
    risk_per_trade = capital * 0.02
    position_size = int(risk_per_trade / (price - stop_loss)) if price > stop_loss else 0

    return {
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "position_size": position_size
    }
