"""A/B Testing Framework"""
from scipy import stats
import numpy as np

# Simulate A/B test data
np.random.seed(42)

# Control group (A)
control_conversions = np.random.binomial(1, 0.10, 1000)  # 10% conversion
# Treatment group (B)
treatment_conversions = np.random.binomial(1, 0.12, 1000)  # 12% conversion

# Calculate statistics
control_rate = control_conversions.mean()
treatment_rate = treatment_conversions.mean()
lift = (treatment_rate - control_rate) / control_rate * 100

# Chi-square test
contingency = np.array([
    [control_conversions.sum(), len(control_conversions) - control_conversions.sum()],
    [treatment_conversions.sum(), len(treatment_conversions) - treatment_conversions.sum()]
])

chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

print("🧪 A/B TEST RESULTS\n")
print(f"Control (A):   {control_rate:.2%} conversion ({control_conversions.sum()}/{len(control_conversions)})")
print(f"Treatment (B): {treatment_rate:.2%} conversion ({treatment_conversions.sum()}/{len(treatment_conversions)})")
print(f"\nLift: {lift:+.2f}%")
print(f"P-value: {p_value:.4f}")
print(f"Significant: {'YES ✅' if p_value < 0.05 else 'NO ❌'}")
