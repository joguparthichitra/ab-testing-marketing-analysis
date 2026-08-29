import pandas as pd

df = pd.read_csv(r"C:\Users\chithra\OneDrive\Desktop\ab_testing_project\data\marketing_AB.csv")

print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df['test group'].value_counts())
# Conversion rate per group
conversion_rates = df.groupby('test group')['converted'].mean()
print(conversion_rates)

# Raw counts: converted vs not, per group (needed for the chi-square test next)
contingency_table = pd.crosstab(df['test group'], df['converted'])
print(contingency_table)
from scipy.stats import chi2_contingency

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("Chi-square statistic:", chi2)
print("P-value:", p_value)
import numpy as np

# Conversion rates and sample sizes per group
p_ad = 14423 / 564577
p_psa = 420 / 23524
n_ad = 564577
n_psa = 23524

# Difference in conversion rates
diff = p_ad - p_psa

# Standard error of the difference
se = np.sqrt((p_ad * (1 - p_ad) / n_ad) + (p_psa * (1 - p_psa) / n_psa))

# 95% confidence interval (1.96 = z-score for 95% confidence)
ci_lower = diff - 1.96 * se
ci_upper = diff + 1.96 * se

print("Conversion rate difference:", diff)
print("95% Confidence Interval:", (ci_lower, ci_upper))
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Effect size (Cohen's h) between the two conversion rates
effect_size = proportion_effectsize(p_ad, p_psa)

# How much statistical power did this test actually have, given its real sample sizes?
analysis = NormalIndPower()
achieved_power = analysis.power(effect_size=effect_size, nobs1=n_psa, ratio=n_ad/n_psa, alpha=0.05)

print("Effect size (Cohen's h):", effect_size)
print("Achieved power:", achieved_power)

# Reverse question: what's the MINIMUM sample size (per group, equal groups) needed to detect this effect at 80% power?
required_n = analysis.solve_power(effect_size=effect_size, power=0.8, ratio=1, alpha=0.05)
print("Required sample size per group (for 80% power, equal groups):", required_n)