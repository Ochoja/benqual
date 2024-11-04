#!/usr/bin/env python3
from api.utils import Utils

# Initialize the Utils object
utils = Utils()

# Extract numbers and first digits from the CSV file
nums = utils.extract_csv_values("uploads/test.csv", "Test")
first_digits = utils.extract_first_digits(nums)

# Use Utils methods to get observed frequencies and expected percentages
observed_frequencies = utils.count_digits(first_digits)

# --- Kolmogorov-Smirnov Test and MAD Calculation ---
# Use the new methods from Utils
ks_statistic, ks_p_value = utils.get_ks_test(first_digits)
mad = utils.get_mad(first_digits)

# Output the results
print("First Digits:", first_digits)
print("Observed Frequencies:", observed_frequencies)
print("Kolmogorov-Smirnov Statistic (D):", ks_statistic)
print("P-Value:", ks_p_value)
print("Mean Absolute Deviation (MAD):", mad)
