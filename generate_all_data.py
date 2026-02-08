"""
Standalone script to generate all datasets and run analysis.
Equivalent to running all notebooks in sequence.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from uuid import uuid4
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
print("=" * 60)
print("📊 SOCIAL MEDIA ROI ATTRIBUTION - DATA GENERATION")
print("=" * 60)

# Configuration
N_INFLUENCERS = 1500
N_POSTS = 50000
N_BRANDS = 25
N_CONVERSIONS = 30000
N_TOUCHPOINTS = 100000
DATE_START = "2024-02-01"
DATE_END = "2025-01-31"

PLATFORM_DIST = {"Instagram": 0.45, "TikTok": 0.35, "YouTube": 0.12, "Twitter": 0.08}
TIER_DIST = {"nano": 0.40, "micro": 0.35, "mid": 0.15, "macro": 0.07, "mega": 0.03}
TIER_FOLLOWERS = {"nano": (1000, 10000), "micro": (10000, 100000), "mid": (100000, 500000), "macro": (500000, 1000000), "mega": (1000000, 10000000)}
TIER_ENGAGEMENT = {"nano": (6.0, 1.5), "micro": (3.5, 1.0), "mid": (2.2, 0.6), "macro": (1.5, 0.4), "mega": (1.0, 0.3)}
TIER_AUTHENTICITY = {"nano": (0.92, 0.05), "micro": (0.88, 0.06), "mid": (0.82, 0.08), "macro": (0.75, 0.10), "mega": (0.70, 0.12)}
TIER_COST = {"nano": (50, 150), "micro": (150, 1000), "mid": (1000, 5000), "macro": (5000, 15000), "mega": (15000, 100000)}
GENDER_DIST = {"Female": 0.48, "Male": 0.45, "Non-binary": 0.05, "Unknown": 0.02}
COUNTRY_DIST = {"United States": 0.30, "United Kingdom": 0.12, "Germany": 0.08, "France": 0.07, "Italy": 0.05, "Spain": 0.05, "Australia": 0.05, "Canada": 0.05, "Japan": 0.04, "South Korea": 0.04, "Brazil": 0.04, "India": 0.04, "Mexico": 0.03, "Netherlands": 0.02, "Sweden": 0.02}
AGE_DIST = {"18-24": 0.35, "25-34": 0.40, "35-44": 0.18, "45+": 0.07}
CONTENT_CATEGORIES = ["Luxury Fashion", "Streetwear", "Sustainable Fashion", "Fast Fashion", "Accessories", "Footwear", "Activewear", "Vintage/Thrift"]
VISUAL_STYLES = {"lifestyle": 0.35, "product_shot": 0.30, "behind_scenes": 0.15, "user_generated": 0.12, "editorial": 0.08}
BRAND_TIERS = {"Luxury": 0.20, "Premium": 0.25, "Mid-market": 0.30, "Fast-fashion": 0.15, "DTC": 0.10}
BRAND_AOV = {"Luxury": (500, 2000), "Premium": (150, 500), "Mid-market": (50, 150), "Fast-fashion": (25, 75), "DTC": (75, 200)}
SEASONALITY = {1: 0.85, 2: 0.90, 3: 0.95, 4: 1.00, 5: 0.95, 6: 0.85, 7: 0.80, 8: 0.90, 9: 1.05, 10: 1.10, 11: 1.20, 12: 1.25}
COLORS = ["neutral_beige", "cream_white", "classic_black", "navy_blue", "olive_green", "terracotta", "dusty_rose", "burgundy", "camel_brown", "sage_green"]
CONTENT_TYPES = {"Instagram": {"photo": 0.35, "carousel": 0.25, "reel": 0.30, "story": 0.10}, "TikTok": {"video": 0.95, "photo": 0.05}, "YouTube": {"video": 0.85, "shorts": 0.15}, "Twitter": {"photo": 0.50, "video": 0.25, "text": 0.25}}

def sample_dist(dist, n=1):
    return np.random.choice(list(dist.keys()), size=n, p=list(dist.values()))

def gen_followers(tier):
    low, high = TIER_FOLLOWERS[tier]
    return int(np.exp(np.random.uniform(np.log(low), np.log(high))))

def gen_engagement(tier):
    mean, std = TIER_ENGAGEMENT[tier]
    return np.clip(np.random.normal(mean, std), 0.5, 12.0)

def gen_authenticity(tier):
    mean, std = TIER_AUTHENTICITY[tier]
    return np.clip(np.random.normal(mean, std), 0.4, 0.99)

def gen_cost(tier, followers):
    low, high = TIER_COST[tier]
    tier_range = TIER_FOLLOWERS[tier]
    position = (followers - tier_range[0]) / (tier_range[1] - tier_range[0])
    return round((low + position * (high - low)) * np.random.uniform(0.8, 1.2), 2)

def gen_engagement_metrics(followers, eng_rate, is_viral=False):
    variance = np.random.uniform(0.7, 1.3) * (np.random.uniform(3, 10) if is_viral else 1)
    total = int(followers * (eng_rate / 100) * variance)
    likes = max(1, int(total * np.random.uniform(0.85, 0.92)))
    comments = max(0, int(likes * np.random.uniform(0.03, 0.08)))
    shares = max(0, int(likes * np.random.uniform(0.01, 0.025)))
    saves = max(0, int(likes * np.random.uniform(0.02, 0.05)))
    return likes, comments, shares, saves

def gen_order_value(brand_tier):
    low, high = BRAND_AOV[brand_tier]
    value = np.exp(np.random.normal((np.log(low) + np.log(high)) / 2, (np.log(high) - np.log(low)) / 4))
    return round(np.clip(value, low * 0.5, high * 1.5), 2)

# Create directories
data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Generate Brands
print("\n🏢 Generating Brands...")
brand_prefixes = ["Maison", "Atelier", "Casa", "Studio", "House of", "La", "Le", "The", "Modern", "Luxe"]
brand_suffixes = ["Mode", "Style", "Vogue", "Chic", "Edit", "Label", "Collective", "Co", "Design", "Wear"]
brands = []
tiers = sample_dist(BRAND_TIERS, N_BRANDS)
for i in range(N_BRANDS):
    tier = tiers[i]
    budget_ranges = {"Luxury": (200000, 500000), "Premium": (100000, 250000), "Mid-market": (50000, 150000), "Fast-fashion": (75000, 200000), "DTC": (25000, 100000)}
    low, high = budget_ranges[tier]
    brands.append({
        "brand_id": str(uuid4()), "brand_name": f"{np.random.choice(brand_prefixes)} {np.random.choice(brand_suffixes)}",
        "brand_tier": tier, "monthly_social_budget": round(np.random.uniform(low, high), 2),
        "primary_platform": sample_dist(PLATFORM_DIST)[0], "avg_product_price": gen_order_value(tier),
        "target_demographic": np.random.choice(["18-24", "25-34", "35-44", "25-44"]), "founded_year": np.random.randint(1990, 2022)
    })
brands_df = pd.DataFrame(brands)
print(f"   ✅ {len(brands_df)} brands")

# Generate Influencers
print("👤 Generating Influencers...")
influencers = []
tiers = sample_dist(TIER_DIST, N_INFLUENCERS)
platforms = sample_dist(PLATFORM_DIST, N_INFLUENCERS)
countries = sample_dist(COUNTRY_DIST, N_INFLUENCERS)
genders = sample_dist(GENDER_DIST, N_INFLUENCERS)
ages = sample_dist(AGE_DIST, N_INFLUENCERS)
for i in range(N_INFLUENCERS):
    tier = tiers[i]
    followers = gen_followers(tier)
    influencers.append({
        "influencer_id": str(uuid4()), "username": f"creator_{i+1:05d}", "platform": platforms[i],
        "tier": tier, "follower_count": followers, "engagement_rate": round(gen_engagement(tier), 2),
        "country": countries[i], "content_category": np.random.choice(CONTENT_CATEGORIES),
        "avg_post_frequency": round(np.clip(np.random.normal(4.2, 1.5), 1, 10), 1),
        "audience_authenticity_score": round(gen_authenticity(tier), 2),
        "avg_collaboration_cost": gen_cost(tier, followers), "account_age_months": np.random.randint(12, 96),
        "gender": genders[i], "age_group": ages[i],
        "verified": np.random.random() < (0.1 if tier in ["nano", "micro"] else 0.5), "active": np.random.random() < 0.95
    })
influencers_df = pd.DataFrame(influencers)
print(f"   ✅ {len(influencers_df)} influencers")

# Generate Posts
print("📱 Generating Posts...")
start_date = datetime.strptime(DATE_START, "%Y-%m-%d")
end_date = datetime.strptime(DATE_END, "%Y-%m-%d")
date_range = (end_date - start_date).days
inf_ids = influencers_df["influencer_id"].tolist()
brand_ids = brands_df["brand_id"].tolist()
inf_lookup = influencers_df.set_index("influencer_id").to_dict("index")
posts = []
for i in range(N_POSTS):
    inf_id = np.random.choice(inf_ids)
    inf = inf_lookup[inf_id]
    platform = inf["platform"]
    post_date = start_date + timedelta(days=np.random.randint(0, date_range))
    month = post_date.month
    content_types = CONTENT_TYPES.get(platform, {"photo": 1.0})
    content_type = sample_dist(content_types)[0]
    is_sponsored = np.random.random() < (0.25 if inf["tier"] in ["mid", "macro", "mega"] else 0.10)
    is_viral = np.random.random() < 0.05
    eng_rate = inf["engagement_rate"] * SEASONALITY[month]
    likes, comments, shares, saves = gen_engagement_metrics(inf["follower_count"], eng_rate, is_viral)
    reach = int(inf["follower_count"] * np.random.uniform(0.20, 0.40))
    posts.append({
        "post_id": str(uuid4()), "influencer_id": inf_id, "brand_id": np.random.choice(brand_ids) if is_sponsored else None,
        "platform": platform, "post_date": post_date.strftime("%Y-%m-%d"),
        "post_time_hour": np.random.randint(6, 24),
        "day_of_week": np.random.choice(range(7), p=[0.12, 0.16, 0.17, 0.16, 0.14, 0.13, 0.12]),
        "content_type": content_type, "caption_length": int(np.clip(np.random.normal(180, 80), 20, 500)),
        "hashtag_count": int(np.clip(np.random.normal(8 if platform == "Instagram" else 4, 3), 1, 30)),
        "has_cta": np.random.random() < 0.45, "product_count": np.random.poisson(2) if is_sponsored else 0,
        "visual_style": sample_dist(VISUAL_STYLES)[0], "dominant_color": np.random.choice(COLORS),
        "is_sponsored": is_sponsored, "discount_code_present": is_sponsored and np.random.random() < 0.30,
        "likes": likes, "comments": comments, "shares": shares, "saves": saves,
        "reach": reach, "impressions": int(reach * np.random.uniform(1.2, 1.8))
    })
    if (i + 1) % 10000 == 0:
        print(f"   ... {i+1:,} posts")
posts_df = pd.DataFrame(posts)
print(f"   ✅ {len(posts_df)} posts")

# Generate Conversions
print("🛒 Generating Conversions...")
sponsored_posts = posts_df[posts_df["is_sponsored"] == True].copy()
brand_lookup = brands_df.set_index("brand_id").to_dict("index")
product_categories = ["Clothing", "Accessories", "Footwear", "Bags", "Jewelry"]
conversions = []
for i in range(N_CONVERSIONS):
    has_attribution = np.random.random() < 0.65
    if has_attribution and len(sponsored_posts) > 0:
        post = sponsored_posts.sample(1).iloc[0]
        post_id, influencer_id, brand_id = post["post_id"], post["influencer_id"], post["brand_id"]
        post_date = datetime.strptime(post["post_date"], "%Y-%m-%d")
        journey_length = int(np.clip(np.random.exponential(7), 1, 90))
        conversion_date = min(post_date + timedelta(days=journey_length), end_date)
    else:
        post_id, influencer_id = None, None
        brand_id = np.random.choice(brand_ids)
        conversion_date = start_date + timedelta(days=np.random.randint(0, date_range))
        journey_length = int(np.clip(np.random.exponential(7), 1, 90))
    brand_tier = brand_lookup[brand_id]["brand_tier"] if brand_id else "Mid-market"
    conversions.append({
        "conversion_id": str(uuid4()), "customer_id": str(uuid4()), "post_id": post_id,
        "influencer_id": influencer_id, "brand_id": brand_id,
        "conversion_date": conversion_date.strftime("%Y-%m-%d"),
        "attribution_type": np.random.choice(["first_touch", "last_touch", "linear", "time_decay", "position_based"], p=[0.15, 0.25, 0.20, 0.25, 0.15]),
        "utm_source": np.random.choice(["instagram", "tiktok", "youtube", "twitter", "direct", "organic"]),
        "utm_medium": np.random.choice(["social", "influencer", "organic", "paid"]),
        "order_value": gen_order_value(brand_tier), "product_category": np.random.choice(product_categories),
        "discount_code_used": post_id is not None and np.random.random() < 0.40,
        "customer_journey_length": journey_length, "touchpoints_count": int(np.clip(np.random.geometric(0.3), 1, 15))
    })
    if (i + 1) % 10000 == 0:
        print(f"   ... {i+1:,} conversions")
conversions_df = pd.DataFrame(conversions)
print(f"   ✅ {len(conversions_df)} conversions")

# Generate Touchpoints
print("🔗 Generating Touchpoints...")
conversions_with_posts = conversions_df[conversions_df["post_id"].notna()].copy()
touchpoint_types = ["view", "click", "save", "like", "comment", "website_visit", "add_to_cart"]
post_ids = posts_df["post_id"].tolist()
touchpoints = []
for i in range(N_TOUCHPOINTS):
    leads_to_conversion = np.random.random() < 0.30
    if leads_to_conversion and len(conversions_with_posts) > 0:
        conv = conversions_with_posts.sample(1).iloc[0]
        conversion_id, customer_id, post_id = conv["conversion_id"], conv["customer_id"], conv["post_id"]
        conv_date = datetime.strptime(conv["conversion_date"], "%Y-%m-%d")
        touchpoint_date = conv_date - timedelta(days=np.random.randint(0, max(1, conv["customer_journey_length"])))
    else:
        conversion_id, customer_id = None, str(uuid4())
        post_id = np.random.choice(post_ids) if np.random.random() < 0.7 else None
        touchpoint_date = start_date + timedelta(days=np.random.randint(0, date_range))
    touchpoints.append({
        "touchpoint_id": str(uuid4()), "customer_id": customer_id, "post_id": post_id,
        "touchpoint_type": np.random.choice(touchpoint_types, p=[0.35, 0.20, 0.10, 0.15, 0.05, 0.10, 0.05]),
        "touchpoint_date": touchpoint_date.strftime("%Y-%m-%d"),
        "platform": np.random.choice(["Instagram", "TikTok", "YouTube", "Twitter", "Website"]),
        "contributed_to_conversion": leads_to_conversion, "conversion_id": conversion_id,
        "attribution_weight": round(np.random.uniform(0.05, 0.40), 3) if leads_to_conversion else 0.0
    })
    if (i + 1) % 25000 == 0:
        print(f"   ... {i+1:,} touchpoints")
touchpoints_df = pd.DataFrame(touchpoints)
print(f"   ✅ {len(touchpoints_df)} touchpoints")

# Save datasets
print("\n💾 Saving datasets...")
brands_df.to_csv(data_dir / "brands.csv", index=False)
influencers_df.to_csv(data_dir / "influencers.csv", index=False)
posts_df.to_csv(data_dir / "posts.csv", index=False)
conversions_df.to_csv(data_dir / "conversions.csv", index=False)
touchpoints_df.to_csv(data_dir / "touchpoints.csv", index=False)

# Validation
print("\n⚖️ BIAS VALIDATION")
print("-" * 40)
gender_dist = influencers_df["gender"].value_counts(normalize=True)
print(f"Gender: F={gender_dist.get('Female', 0):.1%}, M={gender_dist.get('Male', 0):.1%}")
us_share = influencers_df["country"].value_counts(normalize=True).get("United States", 0)
print(f"US representation: {us_share:.1%} (target <35%)")
corr = influencers_df["follower_count"].corr(influencers_df["engagement_rate"])
print(f"Followers ↔ Engagement correlation: {corr:.3f} (should be negative)")

print("\n" + "=" * 60)
print("✅ DATA GENERATION COMPLETE!")
print("=" * 60)
print(f"\n📊 Summary:")
print(f"   brands.csv: {len(brands_df):,} records")
print(f"   influencers.csv: {len(influencers_df):,} records")
print(f"   posts.csv: {len(posts_df):,} records")
print(f"   conversions.csv: {len(conversions_df):,} records")
print(f"   touchpoints.csv: {len(touchpoints_df):,} records")
print(f"\n🚀 Run the dashboard with: python3 -m streamlit run dashboard.py")
