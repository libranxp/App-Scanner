# scanner.py
import os, json, math, time, statistics, datetime
from backend.providers import fmp, finnhub, polygon, lunarcrush, messari, coinmarketcal
from backend.utils import telegram

# ---------- Helpers: BST time ----------
def now_bst_str():
    # BST is UTC+1 in summer; for a simple fixed offset for Actions, use +1
    tz = datetime.timezone(datetime.timedelta(hours=1))
    return datetime.datetime.now(datetime.timezone.utc).astimezone(tz).strftime("%Y-%m-%d %H:%M BST")

# ---------- Technicals ----------
def ema(values, period):
    k = 2 / (period + 1)
    ema_val = None
    out = []
    for v in values:
        if ema_val is None:
            ema_val = v
        else:
            ema_val = v * k + ema_val * (1 - k)
        out.append(ema_val)
    return out

def rsi(closes, period=14):
    if len(closes) < period + 1: return None
    gains, losses = [], []
    for i in range(1, period + 1):
        ch = closes[i] - closes[i-1]
        gains.append(max(ch, 0))
        losses.append(abs(min(ch, 0)))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    rs = (avg_gain / avg_loss) if avg_loss != 0 else 999
    r = 100 - (100 / (1 + rs))
    for i in range(period + 1, len(closes)):
        ch = closes[i] - closes[i-1]
        gain = max(ch, 0); loss = abs(min(ch, 0))
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        rs = (avg_gain / avg_loss) if avg_loss != 0 else 999
        r = 100 - (100 / (1 + rs))
    return r

def bollinger(closes, period=20, mult=2):
    if len(closes) < period: return None
    window = closes[-period:]
    m = statistics.mean(window)
    sd = statistics.pstdev(window) or 0.000001
    upper = m + mult * sd
    lower = m - mult * sd
    return m, upper, lower

def vwap(highs, lows, closes, volumes):
    if not closes: return None
    tp_vol_sum = 0.0
    vol_sum = 0.0
    for h, l, c, v in zip(highs, lows, closes, volumes):
        tp = (h + l + c) / 3.0
        tp_vol_sum += tp * v
        vol_sum += v
    return (tp_vol_sum / vol_sum) if vol_sum else None

def macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal: return None
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line = [a - b for a, b in zip(ema_fast[-len(ema_slow):], ema_slow)]
    signal_line = ema(macd_line, signal)
    hist = macd_line[-1] - signal_line[-1]
    # Recent 3-candle crossover check
    crossed = False
    for i in range(3):
        idx = -1 - i
        try:
            prev = macd_line[idx-1] - signal_line[idx-1]
            cur = macd_line[idx] - signal_line[idx]
            if prev < 0 and cur > 0:
                crossed = True
                break
        except:
            pass
    return hist, crossed

def rvol(volumes, period=20):
    if len(volumes) < period+1: return None
    avg = statistics.mean(volumes[-(period+1):-1]) or 0.000001
    return volumes[-1] / avg

# ---------- Sentiment / Mentions (lightweight, counts only) ----------
def twitter_mentions(symbol: str) -> tuple[int, str]:
    token = os.getenv("TWITTER_BEARER_TOKEN")
    if not token: return 0, ""
    import requests
    headers = {"Authorization": f"Bearer {token}"}
    q = f"({symbol}) lang:en -is:retweet"
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {"query": q, "max_results": 25}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        r.raise_for_status()
        j = r.json()
        count = len(j.get("data", []))
        link = "https://twitter.com/search?q=" + symbol
        return count, link
    except Exception as e:
        print(f"⚠️ Twitter error {symbol}: {e}")
        return 0, ""

def news_headline(symbol: str) -> str:
    key = os.getenv("NEWSAPI_API_KEY")
    if not key: return ""
    import requests
    url = "https://newsapi.org/v2/everything"
    params = {"q": symbol, "pageSize": 1, "language": "en", "apiKey": key, "sortBy": "publishedAt"}
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        j = r.json()
        if j.get("articles"):
            return j["articles"][0].get("url") or ""
    except Exception as e:
        print(f"⚠️ NewsAPI error {symbol}: {e}")
    return ""

def reddit_link(symbol: str) -> str:
    return f"https://www.reddit.com/search/?q={symbol}"

# ---------- Risk & AI ----------
def risk(price: float):
    # ATR-free approximation: 1.5% SL / 3% TP
    sl = price * 0.985
    tp = price * 1.03
    # position sizing placeholder (fixed for alert readability)
    pos = 500
    return sl, tp, pos

def ai_score_from_features(features: dict) -> tuple[float, str]:
    """
    Simple, transparent scoring (0–10) based on live metrics:
      +2 EMA alignment, +2 RSI in band, +2 MACD recent cross, +2 BB signal,
      +1 RVOL threshold, +1 sentiment/catalyst presence
    """
    score = 0.0
    if features.get("ema_alignment"): score += 2
    if 50 <= features.get("rsi", 0) <= 70: score += 2
    if features.get("macd_cross"): score += 2
    if features.get("bb_signal"): score += 2
    if features.get("rvol", 0) >= features.get("rvol_min", 1.2): score += 1
    if features.get("sentiment_ok"): score += 1
    conf = "High" if score >= 8.5 else ("Medium" if score >= 7.5 else "Moderate")
    return score, conf

# ---------- Criteria checks ----------
def passes_stock_criteria(sym, price, change_pct, volumes, highs, lows, closes) -> tuple[bool, dict, str]:
    rsi_v = rsi(closes)
    bb = bollinger(closes)
    macd_hist, macd_cross = macd(closes) if closes else (None, False)
    ema5 = ema(closes, 5)[-1] if closes else None
    ema13 = ema(closes, 13)[-1] if closes else None
    ema50 = ema(closes, 50)[-1] if closes else None
    ema_ok = ema5 and ema13 and ema50 and (ema5 > ema13 > ema50)
    vwap_v = vwap(highs, lows, closes, volumes)
    vwap_ok = abs((closes[-1] - vwap_v) / vwap_v) <= 0.015 if vwap_v else False
    rv = rvol(volumes) or 0.0

    # Stock thresholds
    rvol_min = 1.2
    rsi_ok = rsi_v and 45 <= rsi_v <= 75
    bb_signal = False
    reason = ""
    if bb:
        mid, up, lo = bb
        if closes[-1] > up or closes[-1] < lo:
            bb_signal = True

    # Sentiment
    tw_count, tw_link = twitter_mentions(sym)
    sent_ok = tw_count >= 5
    news_url = news_headline(sym)
    catalyst_ok = bool(news_url)
    catalyst_url = news_url or ""

    features = {
        "ema_alignment": bool(ema_ok),
        "rsi": rsi_v or 0,
        "macd_cross": macd_cross,
        "bb_signal": bb_signal,
        "rvol": rv,
        "rvol_min": rvol_min,
        "sentiment_ok": sent_ok or catalyst_ok
    }
    score, conf = ai_score_from_features(features)

    # Final criteria gate:
    ok = (
        (change_pct is not None and change_pct > 1.0) and
        rsi_ok and macd_cross and bb_signal and
        rv >= rvol_min and ema_ok and vwap_ok and
        score >= 6.5
    )

    if ok:
        reason = "Twitter buzz + RSI band + MACD cross + Volume spike"
    return ok, {
        "rsi": rsi_v, "ema5": ema5, "ema13": ema13, "ema50": ema50,
        "vwap": vwap_v, "rvol": rv, "ai_score": score, "confidence": conf,
        "tw_count": tw_count, "tw_link": tw_link,
        "news_url": news_url, "catalyst_url": catalyst_url
    }, reason

def passes_crypto_criteria(sym, price, change_pct_24h, volumes, highs, lows, closes, vol24, mcap, mentions) -> tuple[bool, dict, str]:
    rsi_v = rsi(closes)
    bb = bollinger(closes)
    macd_hist, macd_cross = macd(closes) if closes else (None, False)
    ema5 = ema(closes, 5)[-1] if closes else None
    ema13 = ema(closes, 13)[-1] if closes else None
    ema50 = ema(closes, 50)[-1] if closes else None
    ema_ok = ema5 and ema13 and ema50 and (ema5 > ema13 > ema50)
    vwap_v = vwap(highs, lows, closes, volumes)
    vwap_ok = abs((closes[-1] - vwap_v) / vwap_v) <= 0.02 if vwap_v else False
    rv = rvol(volumes) or 0.0

    # Crypto thresholds
    rvol_min = 2.0
    rsi_ok = rsi_v and 50 <= rsi_v <= 70
    bb_signal = False
    reason = ""
    if bb:
        mid, up, lo = bb
        if closes[-1] > up or closes[-1] < lo:
            bb_signal = True

    tw_count, tw_link = twitter_mentions(sym)
    sent_ok = (mentions or 0) >= 10 or tw_count >= 10
    # For catalyst, try CoinMarketCal
    cmc_events = coinmarketcal.catalysts_for_symbol(sym, limit=1)
    catalyst_url = (cmc_events[0]["url"] if cmc_events else "")
    catalyst_ok = bool(catalyst_url)

    features = {
        "ema_alignment": bool(ema_ok),
        "rsi": rsi_v or 0,
        "macd_cross": macd_cross,
        "bb_signal": bb_signal,
        "rvol": rv,
        "rvol_min": rvol_min,
        "sentiment_ok": sent_ok or catalyst_ok
    }
    score, conf = ai_score_from_features(features)

    # Required ranges:
    price_ok = 0.001 <= (price or 0) <= 100
    vol_ok = (vol24 or 0) > 10_000_000
    mcap_ok = 10_000_000 <= (mcap or 0) <= 5_000_000_000
    chg_ok = 2 <= (change_pct_24h or 0) <= 20

    ok = (
        price_ok and vol_ok and mcap_ok and chg_ok and
        rsi_ok and macd_cross and bb_signal and
        rv >= rvol_min and ema_ok and vwap_ok and
        (mentions or 0) >= 10 and score >= 6.5
    )

    if ok:
        reason = "Trending on Twitter + RSI breakout + Whale volume"
    return ok, {
        "rsi": rsi_v, "ema5": ema5, "ema13": ema13, "ema50": ema50,
        "vwap": vwap_v, "rvol": rv, "ai_score": score, "confidence": conf,
        "tw_count": tw_count, "tw_link": tw_link,
        "catalyst_url": catalyst_url
    }, reason

# ---------- Main ----------
def run():
    limit_stocks = int(os.getenv("SCAN_LIMIT_STOCKS", "30"))
    limit_crypto = int(os.getenv("SCAN_LIMIT_CRYPTO", "30"))
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    stock_chat = os.getenv("TELEGRAM_STOCKS_CHANNEL_ID", "")
    crypto_chat = os.getenv("TELEGRAM_CRYPTO_CHANNEL_ID", "")

    dashboard = {"generated_at": now_bst_str(), "stocks": [], "crypto": []}

    # ---- STOCKS SOURCING ----
    # Use FMP + Polygon tickers (live), then compute indicators from Finnhub candles
    universe = []
    try:
        universe.extend(fmp.fetch_most_active(limit=limit_stocks))
    except Exception as e:
        print("⚠️ FMP fetch error:", e)
    try:
        universe.extend(polygon.fetch_gainers(limit=limit_stocks))
    except Exception as e:
        print("⚠️ Polygon fetch error:", e)

    # Dedup by symbol
    seen = set()
    live_stocks = []
    for it in universe:
        sym = it["symbol"]
        if sym in seen: continue
        seen.add(sym)
        live_stocks.append(it)
        if len(live_stocks) >= limit_stocks:
            break

    for st in live_stocks:
        sym = st["symbol"]
        try:
            candles = finnhub.fetch_ohlcv(sym, "5", 800)
            if not candles: continue
            closes = candles["c"]; highs = candles["h"]; lows = candles["l"]; vols = candles["v"]
            ok, feat, reason = passes_stock_criteria(
                sym, st["price"], st.get("change_pct"), vols, highs, lows, closes
            )
            if not ok: continue
            sl, tp, pos = risk(st["price"])
            tv = f"https://www.tradingview.com/symbols/{sym}/"
            signal = {
                "symbol": sym,
                "price": st["price"],
                "change_pct": st.get("change_pct", 0.0),
                "rsi": feat["rsi"],
                "ema5": feat["ema5"], "ema13": feat["ema13"], "ema50": feat["ema50"],
                "vwap": feat["vwap"], "rvol": feat["rvol"],
                "ai_score": feat["ai_score"], "confidence": feat["confidence"],
                "validation": reason,
                "entry": st["price"], "exit": sl,
                "tp": tp, "sl": sl,
                "position_size": pos,
                "sentiment_link": feat["tw_link"],
                "catalyst_link": feat["catalyst_url"],
                "news_link": feat["news_url"],
                "tradingview_link": tv,
                "time_bst": now_bst_str()
            }
            dashboard["stocks"].append(signal)

            if token and stock_chat:
                telegram.send_signal(token, stock_chat, {
                    "symbol": sym,
                    "price": st["price"],
                    "change_pct": st.get("change_pct", 0.0),
                    "ai_score": feat["ai_score"], "confidence": feat["confidence"],
                    "reason": reason,
                    "sl": sl, "tp": tp, "position_size": pos,
                    "sentiment_label": "Bullish" if feat["ai_score"] >= 7.5 else "Positive",
                    "catalyst_label": "Catalyst found" if feat["catalyst_url"] else "—",
                    "tradingview_url": tv,
                    "news_url": feat["news_url"] or "https://news.google.com/",
                    "reddit_url": reddit_link(sym),
                    "tweet_url": feat["tw_link"] or f"https://twitter.com/search?q={sym}",
                    "time_bst": now_bst_str()
                })
                telegram.throttle(0.7)
        except Exception as e:
            print(f"⚠️ Stock processing error {sym}: {e}")

    # ---- CRYPTO SOURCING ----
    crypto_universe = []
    try:
        crypto_universe.extend(lunarcrush.fetch_trending(limit=limit_crypto))
    except Exception as e:
        print("⚠️ LunarCrush fetch error:", e)
    try:
        crypto_universe.extend(messari.top_assets(limit=limit_crypto))
    except Exception as e:
        print("⚠️ Messari fetch error:", e)

    # Dedup by symbol
    seen = set()
    live_crypto = []
    for it in crypto_universe:
        sym = it["symbol"]
        if sym in seen: continue
        seen.add(sym)
        # price/volume fields may differ by source
        price = it.get("price")
        vol24 = it.get("volume_usd_24h")
        mcap = it.get("market_cap")
        mentions = it.get("mentions", 0)
        live_crypto.append({"symbol": sym, "price": price, "volume_usd_24h": vol24, "market_cap": mcap, "mentions": mentions})
        if len(live_crypto) >= limit_crypto:
            break

    # For crypto candles we’ll reuse Finnhub if symbol is listed (e.g., COIN), else skip to avoid false calls.
    # If you have another OHLCV provider for crypto candles, plug it here.

    for co in live_crypto:
        sym = co["symbol"]
        try:
            # Skip candles for now if no stock mapping; you can integrate a crypto OHLCV source (e.g., AlphaVantage crypto)
            # Use AlphaVantage crypto candles if available:
            candles = None
            try:
                from backend.providers import alphavantage
                candles = alphavantage.fetch_crypto_ohlcv(sym)
            except Exception as e:
                print(f"ℹ️ AlphaVantage crypto candles not available for {sym}: {e}")

            if not candles:
                # If we cannot get candles we cannot verify indicators; skip quietly
                continue

            closes = candles["c"]; highs = candles["h"]; lows = candles["l"]; vols = candles["v"]
            change_24h = candles.get("change_24h", 0.0)
            ok, feat, reason = passes_crypto_criteria(
                sym, co["price"], change_24h, vols, highs, lows, closes,
                co.get("volume_usd_24h"), co.get("market_cap"), co.get("mentions", 0)
            )
            if not ok: continue
            sl, tp, pos = risk(co["price"])
            tv = f"https://www.tradingview.com/symbols/{sym}USD/"

            signal = {
                "symbol": sym,
                "price": co["price"],
                "change_pct": change_24h,
                "rsi": feat["rsi"],
                "ema5": feat["ema5"], "ema13": feat["ema13"], "ema50": feat["ema50"],
                "vwap": feat["vwap"], "rvol": feat["rvol"],
                "ai_score": feat["ai_score"], "confidence": feat["confidence"],
                "validation": reason,
                "entry": co["price"], "exit": sl,
                "tp": tp, "sl": sl,
                "position_size": pos,
                "sentiment_link": feat["tw_link"],
                "catalyst_link": feat["catalyst_url"],
                "news_link": "",  # add NewsAPI per-coin if you like
                "tradingview_link": tv,
                "time_bst": now_bst_str()
            }
            dashboard["crypto"].append(signal)

            if token and crypto_chat:
                telegram.send_signal(token, crypto_chat, {
                    "symbol": sym,
                    "price": co["price"],
                    "change_pct": change_24h,
                    "ai_score": feat["ai_score"], "confidence": feat["confidence"],
                    "reason": reason,
                    "sl": sl, "tp": tp, "position_size": pos,
                    "sentiment_label": "Bullish" if feat["ai_score"] >= 7.5 else "Positive",
                    "catalyst_label": "Catalyst found" if feat["catalyst_url"] else "—",
                    "tradingview_url": tv,
                    "news_url": "https://news.google.com/",
                    "reddit_url": reddit_link(sym),
                    "tweet_url": feat["tw_link"] or f"https://twitter.com/search?q={sym}",
                    "time_bst": now_bst_str()
                })
                telegram.throttle(0.7)
        except Exception as e:
            print(f"⚠️ Crypto processing error {sym}: {e}")

    # Write dashboard.json for the dashboard page
    with open("dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    print("✅ dashboard.json updated.")

if __name__ == "__main__":
    run()
