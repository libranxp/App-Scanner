import math


def compute_ai_score(asset_type, features):
# Lightweight, deterministic scorer (no training in CI). You can swap with RF/SVM later.
# Normalize features, then weighted sum → 0..10
w = {
'rsi': 0.8, 'macd_cross': 1.2, 'bb_state': 0.7, 'volume_spike_x': 1.4,
'twitter_mentions': 1.0, 'twitter_engagement': 1.0, 'sentiment': 1.4,
'influencer_flag': 0.8, 'catalyst_count': 1.1,
'insider_activity': 0.6 if asset_type=='stock' else 0.0,
}
score = 0.0
score += min(max((features.get('rsi',50)-50)/25, 0), 1) * w['rsi']
score += (1.0 if features.get('macd_cross') else 0.0) * w['macd_cross']
score += (1.0 if features.get('bb_state') in ('squeeze','breakout') else 0.0) * w['bb_state']
score += min(max((features.get('volume_spike_x',1)-1)/2, 0), 1) * w['volume_spike_x']
score += min(features.get('twitter_mentions',0)/50, 1) * w['twitter_mentions']
score += min(features.get('twitter_engagement',0)/500, 1) * w['twitter_engagement']
score += min(max(features.get('sentiment',0.5),0),1) * w['sentiment']
score += (1.0 if features.get('influencer_flag') else 0.0) * w['influencer_flag']
score += min(features.get('catalyst_count',0)/3, 1) * w['catalyst_count']
if asset_type == 'stock':
score += (1.0 if features.get('insider_activity') else 0.0) * w['insider_activity']
# scale to 0..10
score = min(10, round(10 * score / 9.0, 2))
conf = 'High' if score >= 8 else 'Medium' if score >= 6.5 else 'Low'
narrative = (
'Trending on social + momentum setup' if score >= 8 else
'Constructive setup with improving flow' if score >= 6.5 else
'Signals mixed; caution'
)
return {'score': score, 'confidence': conf, 'narrative': narrative}
