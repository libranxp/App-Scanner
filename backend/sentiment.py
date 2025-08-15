from textblob import TextBlob

def analyze_sentiment(text):
    """
    Returns sentiment polarity score between -1 and 1.
    Positive = bullish, Negative = bearish.
    """
    analysis = TextBlob(text)
    return round(analysis.sentiment.polarity, 2)
