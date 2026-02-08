# Data Dictionary

## Overview
This document describes all fields in the synthetic datasets generated for the Social Media ROI Attribution & Influencer Performance Analyzer project.

---

## 1. Brands Dataset (`brands.csv`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `brand_id` | UUID | Unique identifier | `550e8400-e29b-41d4-a716...` |
| `brand_name` | String | Anonymized brand name | `Maison Style` |
| `brand_tier` | Categorical | Market positioning | `Luxury`, `Premium`, `Mid-market`, `Fast-fashion`, `DTC` |
| `monthly_social_budget` | Float | Monthly marketing budget (USD) | `150000.00` |
| `primary_platform` | Categorical | Main social platform | `Instagram`, `TikTok`, `YouTube`, `Twitter` |
| `avg_product_price` | Float | Average product price (USD) | `245.50` |
| `target_demographic` | Categorical | Primary age group | `18-24`, `25-34`, `35-44`, `25-44` |
| `founded_year` | Integer | Year brand established | `2015` |

---

## 2. Influencers Dataset (`influencers.csv`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `influencer_id` | UUID | Unique identifier | `550e8400-e29b-41d4-a716...` |
| `username` | String | Anonymized username | `creator_00042` |
| `platform` | Categorical | Primary platform | `Instagram`, `TikTok`, `YouTube`, `Twitter` |
| `tier` | Categorical | Influencer size tier | `nano`, `micro`, `mid`, `macro`, `mega` |
| `follower_count` | Integer | Number of followers | `45000` |
| `engagement_rate` | Float | Average engagement % | `4.25` |
| `country` | Categorical | Primary audience location | `United States`, `United Kingdom`, etc. |
| `content_category` | Categorical | Fashion niche | `Luxury Fashion`, `Streetwear`, `Sustainable Fashion`, etc. |
| `avg_post_frequency` | Float | Posts per week | `4.2` |
| `audience_authenticity_score` | Float | Estimated real follower % | `0.89` |
| `avg_collaboration_cost` | Float | Cost per sponsored post (USD) | `500.00` |
| `account_age_months` | Integer | Account age in months | `36` |
| `gender` | Categorical | Influencer gender | `Female`, `Male`, `Non-binary`, `Unknown` |
| `age_group` | Categorical | Influencer age range | `18-24`, `25-34`, `35-44`, `45+` |
| `verified` | Boolean | Has verified badge | `True`, `False` |
| `active` | Boolean | Currently active account | `True`, `False` |

### Tier Definitions
| Tier | Follower Range | Avg Engagement Rate |
|------|----------------|---------------------|
| Nano | 1K - 10K | 5-8% |
| Micro | 10K - 100K | 2.5-4.5% |
| Mid | 100K - 500K | 1.5-3% |
| Macro | 500K - 1M | 1-2% |
| Mega | 1M+ | 0.5-1.5% |

---

## 3. Posts Dataset (`posts.csv`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `post_id` | UUID | Unique identifier | `550e8400-e29b-41d4-a716...` |
| `influencer_id` | UUID | FK to influencers | `550e8400-e29b-41d4-a716...` |
| `brand_id` | UUID | FK to brands (nullable) | `550e8400-e29b-41d4-a716...` |
| `platform` | Categorical | Platform posted on | `Instagram`, `TikTok`, etc. |
| `post_date` | Date | Date posted | `2024-06-15` |
| `post_time_hour` | Integer | Hour of day (0-23) | `14` |
| `day_of_week` | Integer | Day (0=Mon, 6=Sun) | `2` |
| `content_type` | Categorical | Type of content | `photo`, `video`, `carousel`, `reel`, `story` |
| `caption_length` | Integer | Caption characters | `180` |
| `hashtag_count` | Integer | Number of hashtags | `8` |
| `has_cta` | Boolean | Has call-to-action | `True`, `False` |
| `product_count` | Integer | Products shown | `2` |
| `visual_style` | Categorical | Visual approach | `lifestyle`, `product_shot`, `behind_scenes`, `user_generated`, `editorial` |
| `dominant_color` | Categorical | Main color palette | `neutral_beige`, `classic_black`, etc. |
| `is_sponsored` | Boolean | Paid partnership | `True`, `False` |
| `discount_code_present` | Boolean | Has tracking code | `True`, `False` |
| `likes` | Integer | Like count | `2500` |
| `comments` | Integer | Comment count | `85` |
| `shares` | Integer | Share count | `42` |
| `saves` | Integer | Save count | `120` |
| `reach` | Integer | Unique viewers | `15000` |
| `impressions` | Integer | Total views | `22000` |

---

## 4. Conversions Dataset (`conversions.csv`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `conversion_id` | UUID | Unique identifier | `550e8400-e29b-41d4-a716...` |
| `customer_id` | UUID | Anonymized customer | `550e8400-e29b-41d4-a716...` |
| `post_id` | UUID | Attributed post (nullable) | `550e8400-e29b-41d4-a716...` |
| `influencer_id` | UUID | Attributed influencer (nullable) | `550e8400-e29b-41d4-a716...` |
| `brand_id` | UUID | Brand purchased from | `550e8400-e29b-41d4-a716...` |
| `conversion_date` | Date | Purchase date | `2024-06-20` |
| `attribution_type` | Categorical | Attribution model | `first_touch`, `last_touch`, `linear`, `time_decay`, `position_based` |
| `utm_source` | Categorical | Traffic source | `instagram`, `tiktok`, `direct`, `organic` |
| `utm_medium` | Categorical | Traffic medium | `social`, `influencer`, `organic`, `paid` |
| `order_value` | Float | Purchase amount (USD) | `125.00` |
| `product_category` | Categorical | Product type | `Clothing`, `Accessories`, `Footwear`, `Bags`, `Jewelry` |
| `discount_code_used` | Boolean | Used influencer code | `True`, `False` |
| `customer_journey_length` | Integer | Days from awareness to purchase | `7` |
| `touchpoints_count` | Integer | Interactions before purchase | `4` |

---

## 5. Touchpoints Dataset (`touchpoints.csv`)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `touchpoint_id` | UUID | Unique identifier | `550e8400-e29b-41d4-a716...` |
| `customer_id` | UUID | Customer identifier | `550e8400-e29b-41d4-a716...` |
| `post_id` | UUID | Related post (nullable) | `550e8400-e29b-41d4-a716...` |
| `touchpoint_type` | Categorical | Type of interaction | `view`, `click`, `save`, `like`, `comment`, `website_visit`, `add_to_cart` |
| `touchpoint_date` | Date | When interaction occurred | `2024-06-18` |
| `platform` | Categorical | Where interaction happened | `Instagram`, `TikTok`, `Website` |
| `contributed_to_conversion` | Boolean | Led to purchase | `True`, `False` |
| `conversion_id` | UUID | FK to conversion (nullable) | `550e8400-e29b-41d4-a716...` |
| `attribution_weight` | Float | Weight in attribution model | `0.25` |

---

## Data Relationships

```
brands (1) ──────< (M) posts
                      │
influencers (1) ──────┘
     │
     └────< (M) conversions ────< (M) touchpoints
```

## Notes on Data Quality
- All IDs are UUIDs with no duplicates
- Foreign keys are validated for referential integrity
- Distributions based on industry benchmarks (Sprout Social, HubSpot, Influencer Marketing Hub)
- Seasonal patterns reflect fashion industry (Q4 peak, summer dip)
- Bias mitigation applied for gender, geography, and age distributions
