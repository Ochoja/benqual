#!/usr/bin/env python3
from api.utils import Utils
import scipy.stats as stats
import numpy as np

# Initialize the Utils object
Utils = Utils()

# Extract numbers and first digits from the CSV file
nums = Utils.extract_csv_values("uploads/test.csv", "Test")
first_digits = Utils.extract_first_digits(nums)

# Count the observed frequencies of each first digit (1 to 9)
observed_frequencies = Utils.count_digits(first_digits)

# Benford's Law expected proportions for digits 1 to 9
expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

# Calculate total observed values
total_observed = sum(observed_frequencies)

# Calculate observed proportions
observed_proportions = [freq / total_observed for freq in observed_frequencies]

# --- Kolmogorov-Smirnov Test Integration ---
# Calculate cumulative observed and expected proportions
cumulative_observed = np.cumsum(observed_proportions)
cumulative_expected = np.cumsum(expected_proportions)

# Calculate the Kolmogorov-Smirnov statistic (D)
ks_statistic = np.max(np.abs(cumulative_observed - cumulative_expected))

# Calculate the p-value using scipy.stats.kstest
p_value = stats.kstest(cumulative_observed, cumulative_expected)[1]

# --- Mean Absolute Deviation (MAD) Integration ---
# Calculate the absolute deviations
absolute_deviations = [abs(o - e) for o, e in zip(observed_proportions, expected_proportions)]

# Calculate the Mean Absolute Deviation (MAD)
mad = sum(absolute_deviations) / len(absolute_deviations)

# Output the results
print("First Digits:", first_digits)
print("Observed Frequencies:", observed_frequencies)
print("Kolmogorov-Smirnov Statistic (D):", ks_statistic)
print("P-Value:", p_value)
print("Mean Absolute Deviation (MAD):", mad)
