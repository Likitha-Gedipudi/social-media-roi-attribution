"""Generate influencer scores for dashboard"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

print("🌟 Generating Influencer Scores...")

data_dir = Path("data/raw")
influencers = pd.read_csv(data_dir / "influencers.csv")
posts = pd.read_csv(data_dir / "posts.csv")
conversions = pd.read_csv(data_dir / "conversions.csv")

# Aggregate post metrics
inf_post_metrics = posts.groupby('influencer_id').agg({
    'post_id': 'count', 'likes': 'sum', 'comments': 'sum', 'saves': 'sum',
    'shares': 'sum', 'reach': 'sum', 'is_sponsored': 'sum'
}).rename(columns={'post_id': 'total_posts', 'is_sponsored': 'sponsored_posts'})

inf_data = influencers.merge(inf_post_metrics, on='influencer_id', how='left')

# Add conversion data
inf_conversions = conversions[conversions['influencer_id'].notna()].groupby('influencer_id').agg({
    'conversion_id': 'count', 'order_value': 'sum'
}).rename(columns={'conversion_id': 'conversions', 'order_value': 'revenue'})
inf_data = inf_data.merge(inf_conversions, on='influencer_id', how='left')
inf_data['conversions'] = inf_data['conversions'].fillna(0)
inf_data['revenue'] = inf_data['revenue'].fillna(0)

# Engagement Quality Score (25%)
inf_data['weighted_engagement'] = inf_data['likes'] + inf_data['comments'] * 2 + inf_data['saves'] * 3 + inf_data['shares'] * 2
inf_data['engagement_quality'] = inf_data['weighted_engagement'] / (inf_data['follower_count'] / 1000)
scaler = MinMaxScaler(feature_range=(0, 100))
inf_data['engagement_quality_score'] = scaler.fit_transform(inf_data[['engagement_quality']].fillna(0))

# Authenticity Score (25%)
inf_data['authenticity_score'] = inf_data['audience_authenticity_score'] * 100

# Conversion Score (30%)
inf_data['conversion_rate'] = np.where(inf_data['sponsored_posts'] > 0, inf_data['conversions'] / inf_data['sponsored_posts'], 0)
inf_data['conversion_score'] = scaler.fit_transform(inf_data[['conversion_rate']].fillna(0))

# ROI Score (15%)
inf_data['total_cost'] = inf_data['avg_collaboration_cost'] * inf_data['sponsored_posts'].fillna(0)
inf_data['roi'] = np.where(inf_data['total_cost'] > 0, (inf_data['revenue'] - inf_data['total_cost']) / inf_data['total_cost'], 0)
inf_data['roi_capped'] = inf_data['roi'].clip(-1, 10)
inf_data['roi_score'] = scaler.fit_transform(inf_data[['roi_capped']].fillna(0))

# Brand Alignment Score (5%)
alignment_scores = {'Luxury Fashion': 95, 'Streetwear': 85, 'Sustainable Fashion': 90, 'Fast Fashion': 80,
                    'Accessories': 85, 'Footwear': 82, 'Activewear': 78, 'Vintage/Thrift': 88}
inf_data['brand_alignment_score'] = inf_data['content_category'].map(alignment_scores).fillna(75)

# Composite Score
inf_data['influencer_score'] = (0.25 * inf_data['engagement_quality_score'] + 0.25 * inf_data['authenticity_score'] +
                                 0.30 * inf_data['conversion_score'] + 0.15 * inf_data['roi_score'] +
                                 0.05 * inf_data['brand_alignment_score'])

# Segment
inf_data['performance_segment'] = inf_data['influencer_score'].apply(
    lambda x: 'High Performer' if x >= 75 else ('Medium Performer' if x >= 50 else 'Low Performer'))

# Save
output_cols = ['influencer_id', 'username', 'platform', 'tier', 'follower_count', 'engagement_rate',
               'audience_authenticity_score', 'avg_collaboration_cost', 'total_posts', 'sponsored_posts',
               'conversions', 'revenue', 'engagement_quality_score', 'authenticity_score', 'conversion_score',
               'roi_score', 'brand_alignment_score', 'influencer_score', 'performance_segment']
Path("data/processed").mkdir(parents=True, exist_ok=True)
inf_data[output_cols].to_csv("data/processed/influencer_scores.csv", index=False)

print(f"✅ Scored {len(inf_data)} influencers")
print(f"   High Performers: {(inf_data['performance_segment']=='High Performer').sum()}")
print(f"   Medium Performers: {(inf_data['performance_segment']=='Medium Performer').sum()}")
print(f"   Low Performers: {(inf_data['performance_segment']=='Low Performer').sum()}")
print("💾 Saved to data/processed/influencer_scores.csv")
