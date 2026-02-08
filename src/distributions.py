"""
Distribution functions for generating realistic synthetic data.
Based on industry research and statistical distributions.
"""

import numpy as np
from typing import Tuple, Dict, List
import config


def sample_from_distribution(distribution: Dict[str, float], size: int = 1) -> np.ndarray:
    """Sample from a categorical distribution."""
    categories = list(distribution.keys())
    probabilities = list(distribution.values())
    return np.random.choice(categories, size=size, p=probabilities)


def generate_follower_count(tier: str) -> int:
    """Generate follower count based on tier with log-normal distribution."""
    low, high = config.TIER_FOLLOWER_RANGES[tier]
    # Use log-normal for more realistic distribution (right-skewed)
    log_low, log_high = np.log(low), np.log(high)
    log_followers = np.random.uniform(log_low, log_high)
    return int(np.exp(log_followers))


def generate_engagement_rate(tier: str, add_noise: bool = True) -> float:
    """Generate engagement rate based on tier with realistic variance."""
    mean, std = config.TIER_ENGAGEMENT_RATES[tier]
    rate = np.random.normal(mean, std)
    
    if add_noise:
        # Add small random noise for realism
        noise = np.random.uniform(-0.3, 0.3)
        rate += noise
    
    # Ensure rate is within realistic bounds
    return np.clip(rate, 0.5, 12.0)


def generate_authenticity_score(tier: str) -> float:
    """Generate audience authenticity score based on tier."""
    mean, std = config.TIER_AUTHENTICITY_SCORES[tier]
    score = np.random.normal(mean, std)
    return np.clip(score, 0.4, 0.99)


def generate_cost_per_post(tier: str, followers: int) -> float:
    """Generate cost per post based on tier and follower count."""
    low, high = config.TIER_COST_PER_POST[tier]
    # Cost scales with followers within tier
    tier_range = config.TIER_FOLLOWER_RANGES[tier]
    position = (followers - tier_range[0]) / (tier_range[1] - tier_range[0])
    base_cost = low + position * (high - low)
    # Add variance
    variance = np.random.uniform(0.8, 1.2)
    return round(base_cost * variance, 2)


def generate_engagement_metrics(
    followers: int,
    engagement_rate: float,
    content_type: str,
    is_viral: bool = False
) -> Dict[str, int]:
    """
    Generate realistic engagement metrics (likes, comments, shares, saves).
    
    Engagement breakdown:
    - Likes: 85-90% of total engagement
    - Comments: 3-8% of likes
    - Shares: 1-2% of likes
    - Saves: 2-5% of likes (higher for product content)
    """
    # Calculate total engagement
    base_engagement = int(followers * (engagement_rate / 100))
    
    # Add variance
    variance = np.random.uniform(0.7, 1.3)
    if is_viral:
        variance *= np.random.uniform(3, 10)  # Viral posts get 3-10x engagement
    
    total_engagement = int(base_engagement * variance)
    
    # Distribute engagement
    likes = int(total_engagement * np.random.uniform(0.85, 0.92))
    
    # Comments: higher for engaging content
    comment_rate = np.random.uniform(0.03, 0.08)
    comments = int(likes * comment_rate)
    
    # Shares: lower overall
    share_rate = np.random.uniform(0.01, 0.025)
    shares = int(likes * share_rate)
    
    # Saves: higher for product-focused content (indicates purchase intent)
    if content_type in ["product_shot", "carousel"]:
        save_rate = np.random.uniform(0.03, 0.06)
    else:
        save_rate = np.random.uniform(0.02, 0.04)
    saves = int(likes * save_rate)
    
    return {
        "likes": max(1, likes),
        "comments": max(0, comments),
        "shares": max(0, shares),
        "saves": max(0, saves)
    }


def generate_reach_impressions(followers: int, engagement_rate: float) -> Tuple[int, int]:
    """Generate reach and impressions based on followers and engagement."""
    # Reach: typically 20-40% of followers for organic posts
    reach_rate = np.random.uniform(0.20, 0.40)
    
    # Higher engagement = better reach (algorithm boost)
    if engagement_rate > 5:
        reach_rate *= 1.3
    elif engagement_rate > 3:
        reach_rate *= 1.1
    
    reach = int(followers * reach_rate)
    
    # Impressions: 1.2-1.8x reach (people see post multiple times)
    impression_multiplier = np.random.uniform(1.2, 1.8)
    impressions = int(reach * impression_multiplier)
    
    return reach, impressions


def generate_post_time() -> Tuple[int, int]:
    """Generate posting time (hour, day of week) based on optimal times."""
    hour = sample_from_distribution(config.POSTING_TIME_DISTRIBUTION)[0]
    day = sample_from_distribution(config.DAY_OF_WEEK_DISTRIBUTION)[0]
    return int(hour), int(day)


def generate_caption_length() -> int:
    """Generate caption length with normal distribution."""
    length = int(np.random.normal(180, 80))
    return np.clip(length, 20, 500)


def generate_hashtag_count(platform: str) -> int:
    """Generate hashtag count based on platform best practices."""
    if platform == "Instagram":
        count = int(np.random.normal(8, 4))
        return np.clip(count, 1, 30)
    elif platform == "TikTok":
        count = int(np.random.normal(4, 2))
        return np.clip(count, 1, 10)
    elif platform == "Twitter":
        count = int(np.random.normal(2, 1))
        return np.clip(count, 0, 5)
    else:
        return int(np.random.uniform(1, 5))


def generate_order_value(brand_tier: str) -> float:
    """Generate order value based on brand tier using log-normal distribution."""
    low, high = config.BRAND_AOV[brand_tier]
    # Log-normal for realistic e-commerce order values
    log_low, log_high = np.log(low), np.log(high)
    log_value = np.random.normal((log_low + log_high) / 2, (log_high - log_low) / 4)
    value = np.exp(log_value)
    return round(np.clip(value, low * 0.5, high * 1.5), 2)


def generate_customer_journey_length() -> int:
    """Generate customer journey length in days (exponential distribution)."""
    # Most conversions happen quickly, but some take longer
    length = int(np.random.exponential(7))  # Mean of 7 days
    return np.clip(length, 1, 90)


def generate_touchpoints_count() -> int:
    """Generate number of touchpoints in customer journey."""
    # Geometric distribution for touchpoints (most have few, some have many)
    count = int(np.random.geometric(0.3))
    return np.clip(count, 1, 15)


def apply_seasonality(base_value: float, month: int) -> float:
    """Apply seasonal multiplier to a value."""
    seasonality = config.MONTHLY_SEASONALITY.get(month, 1.0)
    return base_value * seasonality


def generate_outlier_probability(tier: str) -> float:
    """Determine if this should be an outlier (viral or underperforming)."""
    # 5-10% of posts are outliers
    if np.random.random() < 0.07:
        return np.random.choice([0.3, 3.0, 5.0], p=[0.3, 0.5, 0.2])  # Under, viral, super-viral
    return 1.0


def generate_attribution_weights(n_touchpoints: int, model: str = "linear") -> List[float]:
    """Generate attribution weights for touchpoints."""
    if model == "first_touch":
        weights = [1.0] + [0.0] * (n_touchpoints - 1)
    elif model == "last_touch":
        weights = [0.0] * (n_touchpoints - 1) + [1.0]
    elif model == "linear":
        weights = [1.0 / n_touchpoints] * n_touchpoints
    elif model == "time_decay":
        # More recent touchpoints get more weight
        raw_weights = [2 ** i for i in range(n_touchpoints)]
        total = sum(raw_weights)
        weights = [w / total for w in raw_weights]
    elif model == "position_based":
        # 40% first, 40% last, 20% middle
        if n_touchpoints == 1:
            weights = [1.0]
        elif n_touchpoints == 2:
            weights = [0.5, 0.5]
        else:
            middle_weight = 0.2 / (n_touchpoints - 2)
            weights = [0.4] + [middle_weight] * (n_touchpoints - 2) + [0.4]
    else:
        weights = [1.0 / n_touchpoints] * n_touchpoints
    
    return weights
