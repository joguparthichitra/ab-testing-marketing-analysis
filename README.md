# Marketing A/B Test Analysis

Statistical analysis of an A/B test measuring whether showing ads (vs. a public service announcement/PSA) increases customer conversion rates.

## Dataset
588,101 users randomly assigned to either see an ad or a PSA. Source: [Kaggle - Marketing A/B Testing](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)

## Methods
- **Chi-square test** to determine if the difference in conversion rates is statistically significant
- **Confidence interval** on the difference in conversion rates
- **Power analysis** (Cohen's h effect size) to evaluate sample size efficiency

## Key Findings
- Ad group conversion rate: 2.55% vs PSA group: 1.79%
- Difference is statistically significant (p < 0.001)
- 95% CI for the difference: 0.60% to 0.94%
- Effect size is small (Cohen's h = 0.053), but the large sample gave the test ~100% power to detect it
- Only ~5,588 users per group would be needed to detect this effect at 80% power, suggesting future tests could use much smaller samples

## Tools Used
Python, pandas, SciPy, statsmodels, Streamlit

## Live Dashboard
https://ab-testing-marketing-analysis-ybgsywnhbhajgxrxuen7hy.streamlit.app

## Run Locally
pip install -r requirements.txt
streamlit run dashboard.py
