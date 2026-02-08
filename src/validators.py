"""
Data validation and bias checking for synthetic datasets.
Ensures data quality and verifies distributions match industry benchmarks.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config


class DataValidator:
    """Validate synthetic data for quality and bias."""
    
    def __init__(self, data_dir: Path = config.RAW_DATA_DIR):
        """Initialize validator with data directory."""
        self.data_dir = data_dir
        self.datasets = {}
        self.validation_results = {}
        
    def load_data(self):
        """Load all datasets from CSV files."""
        print("📂 Loading datasets...")
        
        files = ["brands", "influencers", "posts", "conversions", "touchpoints"]
        for name in files:
            filepath = self.data_dir / f"{name}.csv"
            if filepath.exists():
                self.datasets[name] = pd.read_csv(filepath)
                print(f"   ✅ Loaded {name}.csv: {len(self.datasets[name]):,} records")
            else:
                print(f"   ⚠️ {name}.csv not found")
        
        return self.datasets
    
    def check_distributions(self) -> Dict[str, any]:
        """Check if distributions match expected benchmarks."""
        print("\n" + "=" * 60)
        print("📊 Distribution Validation")
        print("=" * 60)
        
        results = {}
        
        if "influencers" in self.datasets:
            df = self.datasets["influencers"]
            
            # Check tier distribution
            print("\n🔹 Influencer Tier Distribution:")
            actual_tiers = df["tier"].value_counts(normalize=True).to_dict()
            expected_tiers = config.TIER_DISTRIBUTION
            
            tier_results = {}
            for tier in expected_tiers:
                actual = actual_tiers.get(tier, 0)
                expected = expected_tiers[tier]
                diff = abs(actual - expected)
                status = "✅" if diff < 0.05 else "⚠️"
                print(f"   {status} {tier}: {actual:.1%} (expected: {expected:.1%}, diff: {diff:.1%})")
                tier_results[tier] = {"actual": actual, "expected": expected, "diff": diff}
            results["tier_distribution"] = tier_results
            
            # Check engagement rates by tier
            print("\n🔹 Engagement Rates by Tier:")
            for tier in config.TIER_ENGAGEMENT_RATES:
                tier_data = df[df["tier"] == tier]["engagement_rate"]
                if len(tier_data) > 0:
                    actual_mean = tier_data.mean()
                    expected_mean, expected_std = config.TIER_ENGAGEMENT_RATES[tier]
                    diff = abs(actual_mean - expected_mean)
                    status = "✅" if diff < 1.0 else "⚠️"
                    print(f"   {status} {tier}: mean={actual_mean:.2f}% (expected: {expected_mean:.2f}%)")
            
            # Check platform distribution
            print("\n🔹 Platform Distribution:")
            actual_platforms = df["platform"].value_counts(normalize=True).to_dict()
            for platform in config.PLATFORM_DISTRIBUTION:
                actual = actual_platforms.get(platform, 0)
                expected = config.PLATFORM_DISTRIBUTION[platform]
                diff = abs(actual - expected)
                status = "✅" if diff < 0.05 else "⚠️"
                print(f"   {status} {platform}: {actual:.1%} (expected: {expected:.1%})")
        
        if "posts" in self.datasets:
            df = self.datasets["posts"]
            
            # Check content type distribution by platform
            print("\n🔹 Content Type by Platform:")
            for platform in df["platform"].unique():
                platform_posts = df[df["platform"] == platform]
                content_dist = platform_posts["content_type"].value_counts(normalize=True)
                print(f"   {platform}: {dict(content_dist.head(3))}")
        
        self.validation_results["distributions"] = results
        return results
    
    def check_correlations(self) -> Dict[str, float]:
        """Verify expected correlations in the data."""
        print("\n" + "=" * 60)
        print("🔗 Correlation Validation")
        print("=" * 60)
        
        results = {}
        
        if "influencers" in self.datasets:
            df = self.datasets["influencers"]
            
            # Followers vs Engagement (should be negative)
            corr = df["follower_count"].corr(df["engagement_rate"])
            expected = "negative"
            status = "✅" if corr < 0 else "❌"
            print(f"\n   {status} Followers ↔ Engagement: {corr:.3f} (expected: {expected})")
            results["followers_engagement"] = {"correlation": corr, "expected": expected, "valid": corr < 0}
            
            # Followers vs Cost (should be positive)
            corr = df["follower_count"].corr(df["avg_collaboration_cost"])
            expected = "positive"
            status = "✅" if corr > 0 else "❌"
            print(f"   {status} Followers ↔ Cost: {corr:.3f} (expected: {expected})")
            results["followers_cost"] = {"correlation": corr, "expected": expected, "valid": corr > 0}
            
            # Authenticity vs Tier (should show pattern)
            tier_order = {"nano": 0, "micro": 1, "mid": 2, "macro": 3, "mega": 4}
            df["tier_num"] = df["tier"].map(tier_order)
            corr = df["tier_num"].corr(df["audience_authenticity_score"])
            expected = "negative (lower for larger influencers)"
            status = "✅" if corr < 0 else "⚠️"
            print(f"   {status} Tier ↔ Authenticity: {corr:.3f} (expected: {expected})")
            results["tier_authenticity"] = {"correlation": corr, "expected": expected, "valid": corr < 0}
        
        if "posts" in self.datasets:
            df = self.datasets["posts"]
            
            # Likes vs Comments (should be positive)
            corr = df["likes"].corr(df["comments"])
            expected = "positive"
            status = "✅" if corr > 0.5 else "⚠️"
            print(f"   {status} Likes ↔ Comments: {corr:.3f} (expected: {expected})")
            results["likes_comments"] = {"correlation": corr, "expected": expected, "valid": corr > 0.5}
            
            # Saves vs Likes (should be positive)
            corr = df["saves"].corr(df["likes"])
            expected = "positive"
            status = "✅" if corr > 0.5 else "⚠️"
            print(f"   {status} Saves ↔ Likes: {corr:.3f} (expected: {expected})")
            results["saves_likes"] = {"correlation": corr, "expected": expected, "valid": corr > 0.5}
        
        self.validation_results["correlations"] = results
        return results
    
    def check_bias(self) -> Dict[str, any]:
        """Check for demographic and other biases in the data."""
        print("\n" + "=" * 60)
        print("⚖️ Bias Analysis")
        print("=" * 60)
        
        results = {}
        
        if "influencers" in self.datasets:
            df = self.datasets["influencers"]
            
            # Gender distribution
            print("\n🔹 Gender Distribution:")
            gender_dist = df["gender"].value_counts(normalize=True).to_dict()
            for gender, expected in config.GENDER_DISTRIBUTION.items():
                actual = gender_dist.get(gender, 0)
                diff = abs(actual - expected)
                status = "✅" if diff < 0.05 else "⚠️"
                print(f"   {status} {gender}: {actual:.1%} (expected: {expected:.1%})")
            results["gender"] = gender_dist
            
            # Geographic distribution
            print("\n🔹 Geographic Distribution:")
            country_dist = df["country"].value_counts(normalize=True)
            us_share = country_dist.get("United States", 0)
            status = "✅" if us_share < 0.35 else "⚠️ (may be US-centric)"
            print(f"   {status} US representation: {us_share:.1%} (target: <35%)")
            print(f"   Top 5 countries: {dict(country_dist.head(5))}")
            results["geography"] = dict(country_dist)
            
            # Age distribution
            print("\n🔹 Age Group Distribution:")
            age_dist = df["age_group"].value_counts(normalize=True).to_dict()
            for age, expected in config.AGE_GROUP_DISTRIBUTION.items():
                actual = age_dist.get(age, 0)
                diff = abs(actual - expected)
                status = "✅" if diff < 0.05 else "⚠️"
                print(f"   {status} {age}: {actual:.1%} (expected: {expected:.1%})")
            results["age_groups"] = age_dist
            
            # Platform representation across genders
            print("\n🔹 Platform × Gender Cross-tabulation:")
            cross_tab = pd.crosstab(df["platform"], df["gender"], normalize="index")
            print(cross_tab.round(2).to_string())
            
            # Check for any platform heavily skewed by gender
            for platform in cross_tab.index:
                if cross_tab.loc[platform, "Female"] > 0.7 or cross_tab.loc[platform, "Male"] > 0.7:
                    print(f"   ⚠️ {platform} may be gender-skewed")
        
        if "conversions" in self.datasets:
            df = self.datasets["conversions"]
            
            # Attribution distribution
            print("\n🔹 Attribution Type Distribution:")
            attr_dist = df["attribution_type"].value_counts(normalize=True)
            print(f"   {dict(attr_dist)}")
            results["attribution_types"] = dict(attr_dist)
        
        self.validation_results["bias"] = results
        return results
    
    def check_data_quality(self) -> Dict[str, any]:
        """Check for data quality issues."""
        print("\n" + "=" * 60)
        print("🔍 Data Quality Checks")
        print("=" * 60)
        
        results = {}
        
        for name, df in self.datasets.items():
            print(f"\n🔹 {name}:")
            
            # Missing values
            missing = df.isnull().sum()
            missing_pct = (missing / len(df) * 100).round(2)
            cols_with_missing = missing_pct[missing_pct > 0]
            
            if len(cols_with_missing) > 0:
                print(f"   Missing values: {dict(cols_with_missing)}")
            else:
                print(f"   ✅ No unexpected missing values")
            
            # Duplicate IDs
            id_col = f"{name.rstrip('s')}_id" if name != "brands" else "brand_id"
            if id_col in df.columns:
                duplicates = df[id_col].duplicated().sum()
                status = "✅" if duplicates == 0 else "❌"
                print(f"   {status} Duplicate IDs: {duplicates}")
            
            # Numeric columns - check for outliers
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols[:5]:  # Check first 5 numeric columns
                if df[col].std() > 0:
                    z_scores = np.abs(stats.zscore(df[col].dropna()))
                    outliers = (z_scores > 3).sum()
                    pct = outliers / len(df) * 100
                    if pct > 10:
                        print(f"   ⚠️ {col}: {pct:.1f}% outliers (>3 std)")
            
            results[name] = {
                "rows": len(df),
                "columns": len(df.columns),
                "missing_cols": dict(cols_with_missing) if len(cols_with_missing) > 0 else {}
            }
        
        self.validation_results["quality"] = results
        return results
    
    def check_referential_integrity(self) -> Dict[str, bool]:
        """Check foreign key relationships between datasets."""
        print("\n" + "=" * 60)
        print("🔗 Referential Integrity Checks")
        print("=" * 60)
        
        results = {}
        
        if "posts" in self.datasets and "influencers" in self.datasets:
            # Posts should reference valid influencers
            valid_influencers = set(self.datasets["influencers"]["influencer_id"])
            post_influencers = set(self.datasets["posts"]["influencer_id"].dropna())
            invalid = post_influencers - valid_influencers
            status = "✅" if len(invalid) == 0 else "❌"
            print(f"   {status} Posts → Influencers: {len(invalid)} invalid references")
            results["posts_influencers"] = len(invalid) == 0
        
        if "posts" in self.datasets and "brands" in self.datasets:
            # Sponsored posts should reference valid brands
            valid_brands = set(self.datasets["brands"]["brand_id"])
            post_brands = set(self.datasets["posts"]["brand_id"].dropna())
            invalid = post_brands - valid_brands
            status = "✅" if len(invalid) == 0 else "❌"
            print(f"   {status} Posts → Brands: {len(invalid)} invalid references")
            results["posts_brands"] = len(invalid) == 0
        
        if "conversions" in self.datasets and "posts" in self.datasets:
            # Conversions should reference valid posts
            valid_posts = set(self.datasets["posts"]["post_id"])
            conv_posts = set(self.datasets["conversions"]["post_id"].dropna())
            invalid = conv_posts - valid_posts
            status = "✅" if len(invalid) == 0 else "❌"
            print(f"   {status} Conversions → Posts: {len(invalid)} invalid references")
            results["conversions_posts"] = len(invalid) == 0
        
        self.validation_results["referential_integrity"] = results
        return results
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report."""
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)
        
        # Count issues
        total_checks = 0
        passed_checks = 0
        
        # Check correlations
        if "correlations" in self.validation_results:
            for key, val in self.validation_results["correlations"].items():
                total_checks += 1
                if val.get("valid", False):
                    passed_checks += 1
        
        # Check referential integrity
        if "referential_integrity" in self.validation_results:
            for key, val in self.validation_results["referential_integrity"].items():
                total_checks += 1
                if val:
                    passed_checks += 1
        
        print(f"\n   Checks Passed: {passed_checks}/{total_checks}")
        
        if passed_checks == total_checks:
            print("   ✅ All validation checks passed!")
            return "PASS"
        else:
            print("   ⚠️ Some validation checks need attention")
            return "REVIEW"
    
    def run_all_checks(self):
        """Run all validation checks."""
        self.load_data()
        self.check_distributions()
        self.check_correlations()
        self.check_bias()
        self.check_data_quality()
        self.check_referential_integrity()
        return self.generate_report()


def main():
    """Main entry point for validation."""
    parser = argparse.ArgumentParser(description="Validate synthetic data")
    parser.add_argument("--check-distributions", action="store_true", help="Check distribution validity")
    parser.add_argument("--check-correlations", action="store_true", help="Check correlation patterns")
    parser.add_argument("--check-bias", action="store_true", help="Check for data biases")
    parser.add_argument("--all", action="store_true", help="Run all checks")
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.all or not any([args.check_distributions, args.check_correlations, args.check_bias]):
        validator.run_all_checks()
    else:
        validator.load_data()
        if args.check_distributions:
            validator.check_distributions()
        if args.check_correlations:
            validator.check_correlations()
        if args.check_bias:
            validator.check_bias()


if __name__ == "__main__":
    main()
