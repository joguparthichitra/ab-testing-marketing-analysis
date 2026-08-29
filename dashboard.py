import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

st.set_page_config(page_title="A/B Test Analysis: Marketing Campaign", layout="wide")

st.title("📊 Marketing A/B Test: Ad vs PSA")
st.write("Analyzing whether showing ads (vs a public service announcement) increases conversion rates.")

# Load data
df = pd.read_csv("data/marketing_AB.csv")

# Sidebar filter
st.sidebar.header("Filters")
day_filter = st.sidebar.multiselect(
    "Filter by day",
    options=df['most ads day'].unique(),
    default=df['most ads day'].unique()
)
filtered_df = df[df['most ads day'].isin(day_filter)]

# Conversion rates
conversion_rates = filtered_df.groupby('test group')['converted'].mean()
contingency_table = pd.crosstab(filtered_df['test group'], filtered_df['converted'])

col1, col2 = st.columns(2)
with col1:
    st.metric("Ad group conversion rate", f"{conversion_rates.get('ad', 0)*100:.2f}%")
with col2:
    st.metric("PSA group conversion rate", f"{conversion_rates.get('psa', 0)*100:.2f}%")

st.subheader("Conversion Counts")
st.dataframe(contingency_table)

# Chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

st.subheader("Statistical Significance")
st.write(f"**Chi-square statistic:** {chi2:.2f}")
st.write(f"**P-value:** {p_value:.2e}")

if p_value < 0.05:
    st.success("✅ The difference is statistically significant (p < 0.05). The ad likely caused higher conversions, not random chance.")
else:
    st.warning("⚠️ The difference is NOT statistically significant (p ≥ 0.05). Can't confidently say the ad caused the difference.")

# Confidence interval
p_ad = conversion_rates.get('ad', 0)
p_psa = conversion_rates.get('psa', 0)
n_ad = (filtered_df['test group'] == 'ad').sum()
n_psa = (filtered_df['test group'] == 'psa').sum()

if n_ad > 0 and n_psa > 0:
    diff = p_ad - p_psa
    se = np.sqrt((p_ad * (1 - p_ad) / n_ad) + (p_psa * (1 - p_psa) / n_psa))
    ci_lower = diff - 1.96 * se
    ci_upper = diff + 1.96 * se

    st.subheader("Effect Size & Confidence Interval")
    st.write(f"**Conversion rate difference:** {diff*100:.2f} percentage points")
    st.write(f"**95% Confidence Interval:** ({ci_lower*100:.2f}%, {ci_upper*100:.2f}%)")

    # Power analysis
    effect_size = proportion_effectsize(p_ad, p_psa)
    analysis = NormalIndPower()
    required_n = analysis.solve_power(effect_size=effect_size, power=0.8, ratio=1, alpha=0.05)

    st.subheader("Sample Size / Power Analysis")
    st.write(f"**Effect size (Cohen's h):** {effect_size:.4f}")
    st.write(f"**Minimum sample size needed per group (80% power):** {required_n:.0f}")
    st.write(f"**Minimum sample size needed per group (80% power):** {required_n:.0f}")

st.subheader("📌 Business Recommendation")

if p_value < 0.05 and diff > 0:
    st.markdown(f"""
    **Recommendation: Roll out the ad campaign.**
    
    Users who saw the ad converted at **{p_ad*100:.2f}%**, compared to **{p_psa*100:.2f}%** 
    for the control (PSA) group — a lift of **{diff*100:.2f} percentage points** 
    (95% CI: {ci_lower*100:.2f}% to {ci_upper*100:.2f}%).
    
    This difference is **statistically significant** (p = {p_value:.2e}), meaning it is 
    extremely unlikely to be due to random chance.
    
    However, the effect size (Cohen's h = {effect_size:.3f}) is **small** by conventional standards. 
    The large sample size ({n_ad + n_psa:,} users) is what allowed this small effect to be detected 
    with high confidence — a smaller test (~{required_n:.0f} users per group) would likely have 
    been sufficient to detect an effect of this size, suggesting future tests could run leaner 
    without sacrificing reliability.
    """)
else:
    st.markdown("""
    **Recommendation: Do not roll out the ad campaign based on this data.**
    
    The difference between groups is not statistically significant, meaning there isn't 
    strong enough evidence that the ad caused a real change in conversion behavior.
    """)