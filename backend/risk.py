# backend/risk.py
# Dynamic risk/entry/exit calculation (no pre-picked tickers)

from typing import Dict
from backend.providers import finnhub, fmp, polygon


def risk_assessment(symbol: str, asset_type: str = "stock") -> Dict[str, str]:
    """
    Returns a risk/entry/exit assessment based on live market indicators:
    - Current price
    - RSI
    - VWAP
    - ATR (volatility)
    """

    # --- fetch price ---
    try:
        if asset_type == "stock":
            data = finnhub.fetch_stock_data(symbol)
            price = float(data.get("c", 0))  # current price
        else:
            data = polygon.fetch_crypto_price(symbol)
            price = float(data.get("price", 0))
    except Exception:
        price = 0.0

    # --- fetch RSI ---
    try:
        if asset_type == "stock":
            rsi = fmp.fetch_rsi(symbol)
        else:
            rsi = fmp.fetch_rsi(symbol, asset_type="crypto")
    except Exception:
        rsi = 50.0

    # --- fetch VWAP ---
    try:
        if asset_type == "stock":
            vwap = finnhub.fetch_vwap(symbol)
        else:
            vwap = polygon.fetch_crypto_vwap(symbol)
    except Exception:
        vwap = price

    # --- fetch ATR ---
    try:
        atr = fmp.fetch_atr(symbol, asset_type=asset_type)
    except Exception:
        atr = price * 0.02  # fallback: 2% volatility

    # --- calculate entry/exit levels ---
    entry = round(price, 2)
    stop_loss = round(price - (2 * atr), 2)
    take_profit = round(price + (3 * atr), 2)

    # --- risk label ---
    if rsi > 70:
        risk = "Overbought – High risk"
    elif rsi < 30:
        risk = "Oversold – Potential rebound"
    else:
        risk = "Neutral risk zone"

    return {
        "price": str(entry),
        "rsi": str(rsi),
        "vwap": str(round(vwap, 2)),
        "atr": str(round(atr, 2)),
        "entry": str(entry),
        "stop_loss": str(stop_loss),
        "take_profit": str(take_profit),
        "risk_label": risk,
    }
