from statistics import mean


def compute_sentiment(tw=None, reddit=None, news=None):
tw = tw or []; reddit = reddit or []; news = news or []
# Crude proxy: presence and engagement imply positivity; you can replace with VADER or cloud API later.
tw_pos = min(len(tw)/50, 1.0)
rd_pos = min(len(reddit)/30, 1.0)
nw_pos = min(len(news)/20, 1.0)
score = round(0.5 + 0.5*mean([tw_pos, rd_pos, nw_pos]), 2)
influencer_flag = any(getattr(t, 'public_metrics', {}).get('retweet_count', 0) > 50 for t in tw)
label = 'Bullish' if score >= 0.6 else 'Neutral' if score >= 0.45 else 'Bearish'
return {'score': score, 'la
