"""
Social Media ROI Attribution Dashboard
Streamlit application for interactive analytics

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Social Media ROI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data_dir = Path("data/raw")
    
    if not data_dir.exists():
        st.error("⚠️ Data not found! Please run the data generation notebook first.")
        st.stop()
    
    try:
        brands = pd.read_csv(data_dir / "brands.csv")
        influencers = pd.read_csv(data_dir / "influencers.csv")
        posts = pd.read_csv(data_dir / "posts.csv")
        conversions = pd.read_csv(data_dir / "conversions.csv")
        touchpoints = pd.read_csv(data_dir / "touchpoints.csv")
        
        # Parse dates
        posts['post_date'] = pd.to_datetime(posts['post_date'])
        conversions['conversion_date'] = pd.to_datetime(conversions['conversion_date'])
        
        return brands, influencers, posts, conversions, touchpoints
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Load influencer scores if available
@st.cache_data
def load_scores():
    scores_path = Path("data/processed/influencer_scores.csv")
    if scores_path.exists():
        return pd.read_csv(scores_path)
    return None

brands, influencers, posts, conversions, touchpoints = load_data()
influencer_scores = load_scores()

# Sidebar
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Select View", [
    "📈 Executive Summary",
    "👤 Influencer Analysis",
    "📱 Content Performance",
    "🎯 Attribution Analysis",
    "💰 ROI Calculator"
])

# =============================================
# EXECUTIVE SUMMARY
# =============================================
if page == "📈 Executive Summary":
    st.title("📊 Social Media ROI Dashboard")
    st.markdown("### Executive Summary")
    
    # Calculate metrics
    total_revenue = conversions['order_value'].sum()
    total_spend = brands['monthly_social_budget'].sum() * 12
    roi = (total_revenue - total_spend) / total_spend * 100
    total_engagement = posts['likes'].sum() + posts['comments'].sum() + posts['saves'].sum()
    avg_engagement_rate = (total_engagement / posts['reach'].sum()) * 100
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    with col2:
        st.metric("💸 Marketing Spend", f"${total_spend:,.0f}")
    with col3:
        st.metric("📊 Overall ROI", f"{roi:.1f}%", delta=f"{roi:.1f}%")
    with col4:
        st.metric("💫 Avg Engagement Rate", f"{avg_engagement_rate:.2f}%")
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Platform Performance")
        platform_metrics = posts.groupby('platform').agg({
            'likes': 'sum', 'comments': 'sum', 'saves': 'sum', 'reach': 'sum'
        })
        platform_metrics['engagement_rate'] = (
            (platform_metrics['likes'] + platform_metrics['comments'] + platform_metrics['saves']) 
            / platform_metrics['reach'] * 100
        )
        
        fig = px.bar(
            platform_metrics.reset_index(), 
            x='platform', 
            y='engagement_rate',
            color='platform',
            title="Engagement Rate by Platform"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Over Time")
        monthly_revenue = conversions.groupby(conversions['conversion_date'].dt.to_period('M'))['order_value'].sum()
        monthly_revenue.index = monthly_revenue.index.astype(str)
        
        fig = px.line(
            x=monthly_revenue.index, 
            y=monthly_revenue.values,
            title="Monthly Revenue Trend",
            labels={'x': 'Month', 'y': 'Revenue ($)'}
        )
        fig.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tier performance
    st.subheader("Influencer Tier Performance")
    posts_inf = posts.merge(influencers[['influencer_id', 'tier', 'avg_collaboration_cost']], on='influencer_id')
    tier_order = ['nano', 'micro', 'mid', 'macro', 'mega']
    
    tier_metrics = posts_inf.groupby('tier').agg({
        'likes': 'mean', 'comments': 'mean', 'saves': 'mean', 'reach': 'mean'
    }).reindex(tier_order)
    tier_metrics['engagement_rate'] = (
        (tier_metrics['likes'] + tier_metrics['comments'] + tier_metrics['saves']) / tier_metrics['reach'] * 100
    )
    
    fig = px.bar(
        tier_metrics.reset_index(),
        x='tier',
        y='engagement_rate',
        color='tier',
        title="Engagement Rate by Influencer Tier",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================
# INFLUENCER ANALYSIS
# =============================================
elif page == "👤 Influencer Analysis":
    st.title("👤 Influencer Performance Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_platform = st.selectbox("Platform", ["All"] + list(influencers['platform'].unique()))
    with col2:
        selected_tier = st.selectbox("Tier", ["All"] + list(influencers['tier'].unique()))
    with col3:
        min_followers = st.slider("Min Followers", 0, 1000000, 0, step=10000)
    
    # Filter data
    filtered_inf = influencers.copy()
    if selected_platform != "All":
        filtered_inf = filtered_inf[filtered_inf['platform'] == selected_platform]
    if selected_tier != "All":
        filtered_inf = filtered_inf[filtered_inf['tier'] == selected_tier]
    filtered_inf = filtered_inf[filtered_inf['follower_count'] >= min_followers]
    
    st.metric("Influencers Shown", f"{len(filtered_inf):,}")
    
    # Scatter plot
    fig = px.scatter(
        filtered_inf,
        x='follower_count',
        y='engagement_rate',
        color='tier',
        size='avg_collaboration_cost',
        hover_data=['username', 'platform', 'content_category'],
        title="Followers vs Engagement Rate",
        labels={'follower_count': 'Followers', 'engagement_rate': 'Engagement Rate (%)'}
    )
    fig.update_layout(xaxis_type="log")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top influencers table
    st.subheader("Top Influencers by Engagement")
    top_inf = filtered_inf.nlargest(10, 'engagement_rate')[
        ['username', 'platform', 'tier', 'follower_count', 'engagement_rate', 'avg_collaboration_cost']
    ]
    st.dataframe(top_inf, use_container_width=True)
    
    # Influencer scores if available
    if influencer_scores is not None:
        st.subheader("Influencer Effectiveness Scores")
        
        # Merge scores
        scores = influencer_scores.merge(filtered_inf[['influencer_id']], on='influencer_id')
        
        if len(scores) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Score distribution
                fig = px.histogram(
                    scores, 
                    x='influencer_score', 
                    nbins=30,
                    title="Score Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Segment counts
                segment_counts = scores['performance_segment'].value_counts()
                fig = px.pie(
                    values=segment_counts.values,
                    names=segment_counts.index,
                    title="Performance Segments",
                    color_discrete_sequence=['green', 'orange', 'red']
                )
                st.plotly_chart(fig, use_container_width=True)

# =============================================
# CONTENT PERFORMANCE
# =============================================
elif page == "📱 Content Performance":
    st.title("📱 Content Performance Analysis")
    
    # Add engagement metrics
    posts['total_engagement'] = posts['likes'] + posts['comments'] + posts['saves'] + posts['shares']
    posts['engagement_rate'] = posts['total_engagement'] / posts['reach'] * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Content Type Performance")
        content_metrics = posts.groupby('content_type')['engagement_rate'].mean().sort_values(ascending=True)
        fig = px.bar(
            x=content_metrics.values,
            y=content_metrics.index,
            orientation='h',
            title="Engagement Rate by Content Type",
            labels={'x': 'Engagement Rate (%)', 'y': 'Content Type'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Visual Style Performance")
        style_metrics = posts.groupby('visual_style')['engagement_rate'].mean().sort_values(ascending=True)
        fig = px.bar(
            x=style_metrics.values,
            y=style_metrics.index,
            orientation='h',
            title="Engagement Rate by Visual Style",
            labels={'x': 'Engagement Rate (%)', 'y': 'Visual Style'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Posting time heatmap
    st.subheader("📅 Optimal Posting Times")
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    heatmap_data = posts.groupby(['day_of_week', 'post_time_hour'])['engagement_rate'].mean().unstack()
    heatmap_data.index = [day_names[i] for i in heatmap_data.index]
    
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Engagement Rate (%)"),
        title="Engagement Rate by Day & Time",
        color_continuous_scale="RdYlGn"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Color analysis
    st.subheader("🎨 Color Performance")
    color_metrics = posts.groupby('dominant_color')['engagement_rate'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=color_metrics.index,
        y=color_metrics.values,
        title="Engagement Rate by Dominant Color",
        labels={'x': 'Color', 'y': 'Engagement Rate (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================
# ATTRIBUTION ANALYSIS
# =============================================
elif page == "🎯 Attribution Analysis":
    st.title("🎯 Multi-Touch Attribution Analysis")
    
    # Touchpoint analysis
    st.subheader("Customer Journey Touchpoints")
    
    converting_tp = touchpoints[touchpoints['contributed_to_conversion'] == True]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Touchpoint type distribution
        tp_counts = converting_tp['touchpoint_type'].value_counts()
        fig = px.pie(
            values=tp_counts.values,
            names=tp_counts.index,
            title="Touchpoint Types in Converting Journeys"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Platform distribution
        platform_counts = converting_tp['platform'].value_counts()
        fig = px.pie(
            values=platform_counts.values,
            names=platform_counts.index,
            title="Platforms in Converting Journeys"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Journey length analysis
    st.subheader("Customer Journey Length")
    journey_lengths = conversions['customer_journey_length']
    
    fig = px.histogram(
        journey_lengths,
        nbins=30,
        title="Distribution of Customer Journey Length (Days)",
        labels={'value': 'Days', 'count': 'Number of Conversions'}
    )
    fig.add_vline(x=journey_lengths.mean(), line_dash="dash", line_color="red", 
                  annotation_text=f"Mean: {journey_lengths.mean():.1f} days")
    st.plotly_chart(fig, use_container_width=True)
    
    # Attribution type distribution
    st.subheader("Attribution Model Usage")
    attr_dist = conversions['attribution_type'].value_counts()
    fig = px.bar(
        x=attr_dist.index,
        y=attr_dist.values,
        title="Attribution Model Distribution",
        labels={'x': 'Attribution Type', 'y': 'Count'}
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================
# ROI CALCULATOR
# =============================================
elif page == "💰 ROI Calculator":
    st.title("💰 ROI Calculator & Budget Optimizer")
    
    st.markdown("""
    Use this calculator to estimate the ROI of your influencer marketing campaigns 
    and optimize budget allocation across different influencer tiers.
    """)
    
    st.subheader("📊 Budget Allocation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_budget = st.number_input("Total Monthly Budget ($)", min_value=1000, max_value=1000000, value=50000, step=5000)
        
        st.markdown("**Allocate Budget by Tier (%)**")
        nano_pct = st.slider("Nano (1K-10K)", 0, 100, 20)
        micro_pct = st.slider("Micro (10K-100K)", 0, 100, 35)
        mid_pct = st.slider("Mid (100K-500K)", 0, 100, 25)
        macro_pct = st.slider("Macro (500K-1M)", 0, 100, 15)
        mega_pct = st.slider("Mega (1M+)", 0, 100, 5)
        
        total_pct = nano_pct + micro_pct + mid_pct + macro_pct + mega_pct
        if total_pct != 100:
            st.warning(f"⚠️ Total allocation: {total_pct}% (should be 100%)")
    
    with col2:
        st.markdown("**Budget Allocation**")
        
        allocations = {
            'Nano': total_budget * nano_pct / 100,
            'Micro': total_budget * micro_pct / 100,
            'Mid': total_budget * mid_pct / 100,
            'Macro': total_budget * macro_pct / 100,
            'Mega': total_budget * mega_pct / 100
        }
        
        # Show allocation
        for tier, amount in allocations.items():
            st.metric(f"{tier}", f"${amount:,.0f}")
    
    st.divider()
    
    # Estimated results based on historical performance
    st.subheader("📈 Estimated Results")
    
    # Get historical performance by tier
    posts_inf = posts.merge(influencers[['influencer_id', 'tier', 'avg_collaboration_cost']], on='influencer_id')
    
    tier_map = {'nano': 'Nano', 'micro': 'Micro', 'mid': 'Mid', 'macro': 'Macro', 'mega': 'Mega'}
    
    # Calculate estimated metrics
    results = []
    for tier_lower, tier_nice in tier_map.items():
        tier_data = posts_inf[posts_inf['tier'] == tier_lower]
        if len(tier_data) > 0:
            avg_cost = tier_data['avg_collaboration_cost'].mean()
            avg_reach = tier_data['reach'].mean()
            avg_engagement = (tier_data['likes'] + tier_data['comments'] + tier_data['saves']).mean()
            
            budget = allocations[tier_nice]
            estimated_posts = budget / avg_cost if avg_cost > 0 else 0
            estimated_reach = estimated_posts * avg_reach
            estimated_engagement = estimated_posts * avg_engagement
            
            results.append({
                'Tier': tier_nice,
                'Budget': budget,
                'Est. Posts': int(estimated_posts),
                'Est. Reach': int(estimated_reach),
                'Est. Engagement': int(estimated_engagement)
            })
    
    results_df = pd.DataFrame(results)
    st.dataframe(results_df, use_container_width=True)
    
    # Total estimates
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Est. Posts", f"{results_df['Est. Posts'].sum():,}")
    with col2:
        st.metric("Total Est. Reach", f"{results_df['Est. Reach'].sum():,.0f}")
    with col3:
        st.metric("Total Est. Engagement", f"{results_df['Est. Engagement'].sum():,.0f}")

# Footer
st.sidebar.divider()
st.sidebar.markdown("---")
st.sidebar.markdown("**Social Media ROI Attribution**")
st.sidebar.markdown("Built for Fashion Industry Analytics")
