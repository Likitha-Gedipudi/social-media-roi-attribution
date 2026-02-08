"""
Configuration parameters for synthetic data generation.
Based on industry benchmarks from Sprout Social, Later, HubSpot, and Influencer Marketing Hub.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Random seed for reproducibility
RANDOM_SEED = 42

# Dataset sizes
N_INFLUENCERS = 1500
N_POSTS = 50000
N_BRANDS = 25
N_CONVERSIONS = 30000
N_TOUCHPOINTS = 100000

# Date range for data generation (12 months)
DATE_START = "2024-02-01"
DATE_END = "2025-01-31"

# Platform distribution (based on fashion industry usage)
PLATFORM_DISTRIBUTION = {
    "Instagram": 0.45,
    "TikTok": 0.35,
    "YouTube": 0.12,
    "Twitter": 0.08
}

# Influencer tier distribution (industry standard)
TIER_DISTRIBUTION = {
    "nano": 0.40,      # 1K - 10K followers
    "micro": 0.35,     # 10K - 100K followers
    "mid": 0.15,       # 100K - 500K followers
    "macro": 0.07,     # 500K - 1M followers
    "mega": 0.03       # 1M+ followers
}

# Follower ranges by tier
TIER_FOLLOWER_RANGES = {
    "nano": (1000, 10000),
    "micro": (10000, 100000),
    "mid": (100000, 500000),
    "macro": (500000, 1000000),
    "mega": (1000000, 10000000)
}

# Engagement rate benchmarks by tier (mean, std)
# Source: Sprout Social, Later, Influencer Marketing Hub 2024
TIER_ENGAGEMENT_RATES = {
    "nano": (6.0, 1.5),      # 4.5% - 7.5%
    "micro": (3.5, 1.0),     # 2.5% - 4.5%
    "mid": (2.2, 0.6),       # 1.6% - 2.8%
    "macro": (1.5, 0.4),     # 1.1% - 1.9%
    "mega": (1.0, 0.3)       # 0.7% - 1.3%
}

# Audience authenticity by tier (higher for nano, lower for mega)
TIER_AUTHENTICITY_SCORES = {
    "nano": (0.92, 0.05),
    "micro": (0.88, 0.06),
    "mid": (0.82, 0.08),
    "macro": (0.75, 0.10),
    "mega": (0.70, 0.12)
}

# Cost per post by tier (USD) - based on $10-100 per 10K followers
TIER_COST_PER_POST = {
    "nano": (50, 150),
    "micro": (150, 1000),
    "mid": (1000, 5000),
    "macro": (5000, 15000),
    "mega": (15000, 100000)
}

# Content categories for fashion
CONTENT_CATEGORIES = [
    "Luxury Fashion",
    "Streetwear",
    "Sustainable Fashion",
    "Fast Fashion",
    "Accessories",
    "Footwear",
    "Activewear",
    "Vintage/Thrift"
]

# Geographic distribution (avoid US-centric bias)
COUNTRY_DISTRIBUTION = {
    "United States": 0.30,
    "United Kingdom": 0.12,
    "Germany": 0.08,
    "France": 0.07,
    "Italy": 0.05,
    "Spain": 0.05,
    "Australia": 0.05,
    "Canada": 0.05,
    "Japan": 0.04,
    "South Korea": 0.04,
    "Brazil": 0.04,
    "India": 0.04,
    "Mexico": 0.03,
    "Netherlands": 0.02,
    "Sweden": 0.02
}

# Gender distribution (balanced but reflecting fashion industry)
GENDER_DISTRIBUTION = {
    "Female": 0.48,
    "Male": 0.45,
    "Non-binary": 0.05,
    "Unknown": 0.02
}

# Age group distribution for fashion influencers
AGE_GROUP_DISTRIBUTION = {
    "18-24": 0.35,
    "25-34": 0.40,
    "35-44": 0.18,
    "45+": 0.07
}

# Content type by platform
CONTENT_TYPE_BY_PLATFORM = {
    "Instagram": {
        "photo": 0.35,
        "carousel": 0.25,
        "reel": 0.30,
        "story": 0.10
    },
    "TikTok": {
        "video": 0.95,
        "photo": 0.05
    },
    "YouTube": {
        "video": 0.85,
        "shorts": 0.15
    },
    "Twitter": {
        "photo": 0.50,
        "video": 0.25,
        "text": 0.25
    }
}

# Optimal posting times (hour of day, probability)
POSTING_TIME_DISTRIBUTION = {
    6: 0.02, 7: 0.03, 8: 0.05, 9: 0.07, 10: 0.08,
    11: 0.10, 12: 0.12, 13: 0.10, 14: 0.07, 15: 0.06,
    16: 0.05, 17: 0.04, 18: 0.06, 19: 0.08, 20: 0.10,
    21: 0.08, 22: 0.05, 23: 0.03
}

# Day of week distribution (higher on weekdays)
DAY_OF_WEEK_DISTRIBUTION = {
    0: 0.12,  # Monday
    1: 0.16,  # Tuesday
    2: 0.17,  # Wednesday
    3: 0.16,  # Thursday
    4: 0.14,  # Friday
    5: 0.13,  # Saturday
    6: 0.12   # Sunday
}

# Visual styles for fashion content
VISUAL_STYLES = {
    "lifestyle": 0.35,
    "product_shot": 0.30,
    "behind_scenes": 0.15,
    "user_generated": 0.12,
    "editorial": 0.08
}

# Fashion-relevant color palettes
DOMINANT_COLORS = [
    "neutral_beige", "cream_white", "classic_black", "navy_blue",
    "olive_green", "terracotta", "dusty_rose", "burgundy",
    "camel_brown", "sage_green", "lavender", "rust_orange",
    "charcoal_grey", "ivory", "forest_green"
]

# Brand tiers
BRAND_TIERS = {
    "Luxury": 0.20,
    "Premium": 0.25,
    "Mid-market": 0.30,
    "Fast-fashion": 0.15,
    "DTC": 0.10
}

# Average order value by brand tier (USD)
BRAND_AOV = {
    "Luxury": (500, 2000),
    "Premium": (150, 500),
    "Mid-market": (50, 150),
    "Fast-fashion": (25, 75),
    "DTC": (75, 200)
}

# E-commerce conversion rate (industry standard: 2-3%)
CONVERSION_RATE = 0.025

# Engagement to conversion ratios
SAVE_RATE_MULTIPLIER = 1.8  # Saves indicate higher purchase intent
COMMENT_RATE_MULTIPLIER = 1.3

# Seasonality weights for fashion (Q4 peak, summer dip)
MONTHLY_SEASONALITY = {
    1: 0.85,   # January - post-holiday slump
    2: 0.90,   # February
    3: 0.95,   # March - spring arrivals
    4: 1.00,   # April
    5: 0.95,   # May
    6: 0.85,   # June - summer slow
    7: 0.80,   # July - summer slow
    8: 0.90,   # August - back to school
    9: 1.05,   # September - fall fashion
    10: 1.10,  # October
    11: 1.20,  # November - Black Friday
    12: 1.25   # December - holiday peak
}
