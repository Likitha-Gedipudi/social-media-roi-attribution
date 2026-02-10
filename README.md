# Social Media ROI Attribution & Influencer Performance Analyzer

## Project Overview
A comprehensive data analytics project for fashion brands to optimize their social media marketing budget and measure influencer ROI. Features synthetic data generation, multi-touch attribution modeling, influencer scoring, and an interactive Streamlit dashboard.

---

## Project Structure

```
├── data/
│   ├── raw/                          # Generated synthetic datasets
│   │   ├── influencers.csv           # 1,500 influencer profiles
│   │   ├── posts.csv                 # 50,000 social media posts
│   │   ├── brands.csv                # 25 fashion brands
│   │   ├── conversions.csv           # 30,000 e-commerce conversions
│   │   └── touchpoints.csv           # 100,000 attribution touchpoints
│   └── processed/                    # Scored influencer data
│
├── notebooks/
│   ├── 01_data_generation.ipynb      # Generate all synthetic datasets
│   ├── 02_eda.ipynb                  # Exploratory Data Analysis
│   ├── 03_attribution_modeling.ipynb # Multi-touch attribution (6 models)
│   └── 04_influencer_scoring.ipynb   # Influencer effectiveness model
│
├── src/
│   ├── config.py                     # Industry benchmark configurations
│   ├── distributions.py              # Statistical distribution functions
│   ├── data_generator.py             # Synthetic data generation
│   └── validators.py                 # Data quality & bias validators
│
├── docs/
│   ├── data_dictionary.md            # Field descriptions & data types
│   └── industry_benchmarks.md        # Source references for distributions
│
├── dashboard.py                      # Streamlit interactive dashboard
├── generate_all_data.py              # Quick data generation script
├── requirements.txt                  # Python dependencies
└── README.md
```

---

##  Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Likitha-Gedipudi/social-media-roi-attribution.git
cd social-media-roi-attribution

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic data
python generate_all_data.py

# 4. Generate influencer scores
python generate_scores.py

# 5. Launch the dashboard
streamlit run dashboard.py
```

---

## Key Features

### Data Generation
- **Unbiased synthetic data** based on industry benchmarks (Sprout Social, HubSpot, Later)
- **Bias mitigation**: Balanced gender (48/45/5/2%), global geography, realistic platform splits
- **Realistic correlations**: Inverse follower-engagement relationship, tier-based pricing

### Attribution Modeling
- **6 Attribution Models**: First-touch, Last-touch, Linear, Time-decay, Position-based, Markov Chain
- **Customer Journey Analysis**: Touchpoint path reconstruction and channel comparison

### Influencer Scoring
- **Composite Score (0-100)** based on 5 weighted factors:
  - Engagement Quality (25%)
  - Audience Authenticity (25%)
  - Conversion Rate (30%)
  - Cost Efficiency/ROI (15%)
  - Brand Alignment (5%)
- **Performance Segmentation**: High/Medium/Low performer classification

### Interactive Dashboard
- **Executive Summary**: KPIs, platform performance, revenue trends
- **Influencer Analysis**: Filterable scatter plots, tier comparison
- **Content Performance**: Content type analysis, posting time heatmaps
- **Attribution Analysis**: Touchpoint journey visualization
- **ROI Calculator**: Budget optimizer with estimated results

---

## Datasets Overview

| Dataset | Records | Description |
|---------|---------|-------------|
| Influencers | 1,500 | Profiles across Instagram, TikTok, YouTube, Twitter |
| Posts | 50,000 | Social media content with engagement metrics |
| Brands | 25 | Fashion brand profiles (Luxury to DTC) |
| Conversions | 30,000 | E-commerce purchase data with attribution |
| Touchpoints | 100,000 | Customer journey attribution weights |

---

## Tech Stack

| Category | Tools |
|----------|-------|
| **Data Generation** | Python, pandas, numpy, faker |
| **Analysis** | scikit-learn, scipy, statsmodels |
| **Visualization** | matplotlib, seaborn, plotly |
| **Dashboard** | Streamlit |
| **Attribution** | Custom Markov chain implementation |

---

## 📚 Documentation

- [Data Dictionary](docs/data_dictionary.md) - Field descriptions & data types
- [Industry Benchmarks](docs/industry_benchmarks.md) - Sources for realistic distributions

---

## 📄 License
MIT
