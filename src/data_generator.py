"""
Main synthetic data generator for Social Media ROI Attribution project.
Generates unbiased, realistic data based on industry benchmarks.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import config
import distributions as dist


class SyntheticDataGenerator:
    """Generate synthetic datasets for social media ROI analysis."""
    
    def __init__(self, seed: int = config.RANDOM_SEED):
        """Initialize generator with random seed for reproducibility."""
        np.random.seed(seed)
        self.influencers_df = None
        self.brands_df = None
        self.posts_df = None
        self.conversions_df = None
        self.touchpoints_df = None
        
    def generate_all(self, save: bool = True) -> Dict[str, pd.DataFrame]:
        """Generate all datasets in the correct order."""
        print("=" * 60)
        print("🚀 Starting Synthetic Data Generation")
        print("=" * 60)
        
        # Generate in order of dependencies
        print("\n📊 Generating Brands...")
        self.brands_df = self.generate_brands()
        print(f"   ✅ Generated {len(self.brands_df)} brands")
        
        print("\n👤 Generating Influencers...")
        self.influencers_df = self.generate_influencers()
        print(f"   ✅ Generated {len(self.influencers_df)} influencers")
        
        print("\n📱 Generating Posts...")
        self.posts_df = self.generate_posts()
        print(f"   ✅ Generated {len(self.posts_df)} posts")
        
        print("\n🛒 Generating Conversions...")
        self.conversions_df = self.generate_conversions()
        print(f"   ✅ Generated {len(self.conversions_df)} conversions")
        
        print("\n🔗 Generating Touchpoints...")
        self.touchpoints_df = self.generate_touchpoints()
        print(f"   ✅ Generated {len(self.touchpoints_df)} touchpoints")
        
        if save:
            self.save_all()
        
        print("\n" + "=" * 60)
        print("✨ Data Generation Complete!")
        print("=" * 60)
        
        return {
            "brands": self.brands_df,
            "influencers": self.influencers_df,
            "posts": self.posts_df,
            "conversions": self.conversions_df,
            "touchpoints": self.touchpoints_df
        }
    
    def generate_brands(self) -> pd.DataFrame:
        """Generate synthetic brand data."""
        brands = []
        
        # Sample brand tiers
        tiers = dist.sample_from_distribution(config.BRAND_TIERS, config.N_BRANDS)
        
        # Anonymous brand name prefixes
        brand_prefixes = [
            "Maison", "Atelier", "Casa", "Studio", "House of", 
            "La", "Le", "The", "Modern", "Classic", "Urban", "Luxe",
            "Prima", "Bella", "Nova", "Vero", "Alto", "Aria", "Luna"
        ]
        brand_suffixes = [
            "Mode", "Style", "Vogue", "Chic", "Edit", "Label",
            "Collective", "Co", "Design", "Wear", "Fashion", "Threads"
        ]
        
        for i in range(config.N_BRANDS):
            tier = tiers[i]
            brand_name = f"{np.random.choice(brand_prefixes)} {np.random.choice(brand_suffixes)}"
            
            # Budget based on tier
            budget_ranges = {
                "Luxury": (200000, 500000),
                "Premium": (100000, 250000),
                "Mid-market": (50000, 150000),
                "Fast-fashion": (75000, 200000),
                "DTC": (25000, 100000)
            }
            low, high = budget_ranges[tier]
            monthly_budget = np.random.uniform(low, high)
            
            brands.append({
                "brand_id": str(uuid4()),
                "brand_name": brand_name,
                "brand_tier": tier,
                "monthly_social_budget": round(monthly_budget, 2),
                "primary_platform": dist.sample_from_distribution(config.PLATFORM_DISTRIBUTION)[0],
                "avg_product_price": dist.generate_order_value(tier),
                "target_demographic": np.random.choice(["18-24", "25-34", "35-44", "25-44"]),
                "founded_year": np.random.randint(1990, 2022)
            })
        
        return pd.DataFrame(brands)
    
    def generate_influencers(self) -> pd.DataFrame:
        """Generate synthetic influencer data with balanced demographics."""
        influencers = []
        
        # Sample distributions
        tiers = dist.sample_from_distribution(config.TIER_DISTRIBUTION, config.N_INFLUENCERS)
        platforms = dist.sample_from_distribution(config.PLATFORM_DISTRIBUTION, config.N_INFLUENCERS)
        countries = dist.sample_from_distribution(config.COUNTRY_DISTRIBUTION, config.N_INFLUENCERS)
        genders = dist.sample_from_distribution(config.GENDER_DISTRIBUTION, config.N_INFLUENCERS)
        age_groups = dist.sample_from_distribution(config.AGE_GROUP_DISTRIBUTION, config.N_INFLUENCERS)
        categories = np.random.choice(config.CONTENT_CATEGORIES, config.N_INFLUENCERS)
        
        for i in range(config.N_INFLUENCERS):
            tier = tiers[i]
            followers = dist.generate_follower_count(tier)
            engagement_rate = dist.generate_engagement_rate(tier)
            
            influencers.append({
                "influencer_id": str(uuid4()),
                "username": f"creator_{i+1:05d}",
                "platform": platforms[i],
                "tier": tier,
                "follower_count": followers,
                "engagement_rate": round(engagement_rate, 2),
                "country": countries[i],
                "content_category": categories[i],
                "avg_post_frequency": round(np.random.normal(4.2, 1.5), 1),
                "audience_authenticity_score": round(dist.generate_authenticity_score(tier), 2),
                "avg_collaboration_cost": dist.generate_cost_per_post(tier, followers),
                "account_age_months": np.random.randint(12, 96),
                "gender": genders[i],
                "age_group": age_groups[i],
                "verified": np.random.random() < (0.1 if tier in ["nano", "micro"] else 0.5),
                "active": np.random.random() < 0.95
            })
        
        return pd.DataFrame(influencers)
    
    def generate_posts(self) -> pd.DataFrame:
        """Generate synthetic social media posts with realistic patterns."""
        posts = []
        
        # Generate date range
        start_date = datetime.strptime(config.DATE_START, "%Y-%m-%d")
        end_date = datetime.strptime(config.DATE_END, "%Y-%m-%d")
        date_range = (end_date - start_date).days
        
        # Get influencer and brand IDs
        influencer_ids = self.influencers_df["influencer_id"].tolist()
        brand_ids = self.brands_df["brand_id"].tolist()
        
        # Create lookup for influencer data
        inf_lookup = self.influencers_df.set_index("influencer_id").to_dict("index")
        
        for i in range(config.N_POSTS):
            # Select random influencer
            inf_id = np.random.choice(influencer_ids)
            inf_data = inf_lookup[inf_id]
            platform = inf_data["platform"]
            
            # Generate post date with seasonality
            random_days = np.random.randint(0, date_range)
            post_date = start_date + timedelta(days=random_days)
            month = post_date.month
            
            # Get posting time
            hour, day_of_week = dist.generate_post_time()
            
            # Content type based on platform
            content_types = config.CONTENT_TYPE_BY_PLATFORM.get(platform, {"photo": 1.0})
            content_type = dist.sample_from_distribution(content_types)[0]
            
            # Is this a sponsored post?
            is_sponsored = np.random.random() < (0.25 if inf_data["tier"] in ["mid", "macro", "mega"] else 0.10)
            
            # Generate engagement with seasonality
            outlier_mult = dist.generate_outlier_probability(inf_data["tier"])
            base_engagement = dist.generate_engagement_metrics(
                inf_data["follower_count"],
                inf_data["engagement_rate"] * config.MONTHLY_SEASONALITY[month],
                content_type,
                is_viral=(outlier_mult > 2)
            )
            
            # Generate reach and impressions
            reach, impressions = dist.generate_reach_impressions(
                inf_data["follower_count"],
                inf_data["engagement_rate"]
            )
            
            posts.append({
                "post_id": str(uuid4()),
                "influencer_id": inf_id,
                "brand_id": np.random.choice(brand_ids) if is_sponsored else None,
                "platform": platform,
                "post_date": post_date.strftime("%Y-%m-%d"),
                "post_time_hour": hour,
                "day_of_week": day_of_week,
                "content_type": content_type,
                "caption_length": dist.generate_caption_length(),
                "hashtag_count": dist.generate_hashtag_count(platform),
                "has_cta": np.random.random() < 0.45,
                "product_count": np.random.poisson(2) if is_sponsored else 0,
                "visual_style": dist.sample_from_distribution(config.VISUAL_STYLES)[0],
                "dominant_color": np.random.choice(config.DOMINANT_COLORS),
                "is_sponsored": is_sponsored,
                "discount_code_present": is_sponsored and np.random.random() < 0.30,
                "likes": base_engagement["likes"],
                "comments": base_engagement["comments"],
                "shares": base_engagement["shares"],
                "saves": base_engagement["saves"],
                "reach": reach,
                "impressions": impressions
            })
            
            # Progress indicator
            if (i + 1) % 10000 == 0:
                print(f"   ... generated {i+1:,} posts")
        
        return pd.DataFrame(posts)
    
    def generate_conversions(self) -> pd.DataFrame:
        """Generate e-commerce conversion data."""
        conversions = []
        
        # Get sponsored posts (these drive conversions)
        sponsored_posts = self.posts_df[self.posts_df["is_sponsored"] == True].copy()
        
        # Get brand lookup
        brand_lookup = self.brands_df.set_index("brand_id").to_dict("index")
        
        # Generate dates
        start_date = datetime.strptime(config.DATE_START, "%Y-%m-%d")
        end_date = datetime.strptime(config.DATE_END, "%Y-%m-%d")
        date_range = (end_date - start_date).days
        
        # Product categories
        product_categories = ["Clothing", "Accessories", "Footwear", "Bags", "Jewelry"]
        
        for i in range(config.N_CONVERSIONS):
            # Some conversions are attributed to posts, some are not
            has_attribution = np.random.random() < 0.65
            
            if has_attribution and len(sponsored_posts) > 0:
                # Pick a random sponsored post
                post = sponsored_posts.sample(1).iloc[0]
                post_id = post["post_id"]
                influencer_id = post["influencer_id"]
                brand_id = post["brand_id"]
                
                # Conversion happens after post date
                post_date = datetime.strptime(post["post_date"], "%Y-%m-%d")
                journey_length = dist.generate_customer_journey_length()
                conversion_date = min(post_date + timedelta(days=journey_length), end_date)
            else:
                post_id = None
                influencer_id = None
                brand_id = np.random.choice(self.brands_df["brand_id"].tolist())
                random_days = np.random.randint(0, date_range)
                conversion_date = start_date + timedelta(days=random_days)
                journey_length = dist.generate_customer_journey_length()
            
            # Get brand tier for order value
            brand_tier = brand_lookup[brand_id]["brand_tier"] if brand_id else "Mid-market"
            
            conversions.append({
                "conversion_id": str(uuid4()),
                "customer_id": str(uuid4()),
                "post_id": post_id,
                "influencer_id": influencer_id,
                "brand_id": brand_id,
                "conversion_date": conversion_date.strftime("%Y-%m-%d"),
                "attribution_type": np.random.choice(
                    ["first_touch", "last_touch", "linear", "time_decay", "position_based"],
                    p=[0.15, 0.25, 0.20, 0.25, 0.15]
                ),
                "utm_source": np.random.choice(["instagram", "tiktok", "youtube", "twitter", "direct", "organic"]),
                "utm_medium": np.random.choice(["social", "influencer", "organic", "paid"]),
                "order_value": dist.generate_order_value(brand_tier),
                "product_category": np.random.choice(product_categories),
                "discount_code_used": post_id is not None and np.random.random() < 0.40,
                "customer_journey_length": journey_length,
                "touchpoints_count": dist.generate_touchpoints_count()
            })
            
            # Progress indicator
            if (i + 1) % 10000 == 0:
                print(f"   ... generated {i+1:,} conversions")
        
        return pd.DataFrame(conversions)
    
    def generate_touchpoints(self) -> pd.DataFrame:
        """Generate customer journey touchpoint data."""
        touchpoints = []
        
        # Get conversion data
        conversions_with_posts = self.conversions_df[
            self.conversions_df["post_id"].notna()
        ].copy()
        
        touchpoint_types = ["view", "click", "save", "like", "comment", "website_visit", "add_to_cart"]
        
        for i in range(config.N_TOUCHPOINTS):
            # Some touchpoints lead to conversion
            leads_to_conversion = np.random.random() < 0.30
            
            if leads_to_conversion and len(conversions_with_posts) > 0:
                conversion = conversions_with_posts.sample(1).iloc[0]
                conversion_id = conversion["conversion_id"]
                customer_id = conversion["customer_id"]
                post_id = conversion["post_id"]
                
                # Touchpoint date is before conversion
                conv_date = datetime.strptime(conversion["conversion_date"], "%Y-%m-%d")
                days_before = np.random.randint(0, max(1, conversion["customer_journey_length"]))
                touchpoint_date = conv_date - timedelta(days=days_before)
            else:
                conversion_id = None
                customer_id = str(uuid4())
                post_id = np.random.choice(self.posts_df["post_id"].tolist()) if np.random.random() < 0.7 else None
                
                start_date = datetime.strptime(config.DATE_START, "%Y-%m-%d")
                end_date = datetime.strptime(config.DATE_END, "%Y-%m-%d")
                random_days = np.random.randint(0, (end_date - start_date).days)
                touchpoint_date = start_date + timedelta(days=random_days)
            
            # Get platform from post if available
            if post_id:
                post_platform = self.posts_df[self.posts_df["post_id"] == post_id]["platform"].values
                platform = post_platform[0] if len(post_platform) > 0 else np.random.choice(["Instagram", "TikTok", "YouTube", "Twitter"])
            else:
                platform = np.random.choice(["Instagram", "TikTok", "YouTube", "Twitter", "Website"])
            
            touchpoints.append({
                "touchpoint_id": str(uuid4()),
                "customer_id": customer_id,
                "post_id": post_id,
                "touchpoint_type": np.random.choice(touchpoint_types, p=[0.35, 0.20, 0.10, 0.15, 0.05, 0.10, 0.05]),
                "touchpoint_date": touchpoint_date.strftime("%Y-%m-%d"),
                "platform": platform,
                "contributed_to_conversion": leads_to_conversion,
                "conversion_id": conversion_id,
                "attribution_weight": round(np.random.uniform(0.05, 0.40), 3) if leads_to_conversion else 0.0
            })
            
            # Progress indicator
            if (i + 1) % 25000 == 0:
                print(f"   ... generated {i+1:,} touchpoints")
        
        return pd.DataFrame(touchpoints)
    
    def save_all(self):
        """Save all datasets to CSV files."""
        print("\n💾 Saving datasets to CSV...")
        
        self.brands_df.to_csv(config.RAW_DATA_DIR / "brands.csv", index=False)
        print(f"   ✅ Saved brands.csv")
        
        self.influencers_df.to_csv(config.RAW_DATA_DIR / "influencers.csv", index=False)
        print(f"   ✅ Saved influencers.csv")
        
        self.posts_df.to_csv(config.RAW_DATA_DIR / "posts.csv", index=False)
        print(f"   ✅ Saved posts.csv")
        
        self.conversions_df.to_csv(config.RAW_DATA_DIR / "conversions.csv", index=False)
        print(f"   ✅ Saved conversions.csv")
        
        self.touchpoints_df.to_csv(config.RAW_DATA_DIR / "touchpoints.csv", index=False)
        print(f"   ✅ Saved touchpoints.csv")
        
        print(f"\n   📁 All files saved to: {config.RAW_DATA_DIR}")


def main():
    """Main entry point for data generation."""
    generator = SyntheticDataGenerator()
    datasets = generator.generate_all(save=True)
    
    # Print summary statistics
    print("\n📈 Dataset Summary:")
    print("-" * 40)
    for name, df in datasets.items():
        print(f"   {name}: {len(df):,} records, {len(df.columns)} columns")
    
    return datasets


if __name__ == "__main__":
    main()
