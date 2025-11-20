import pandas as pd
from scipy.stats import chisquare, kstest
import numpy as np

class Utils:
    """Benford's law Utility Functions"""

    def count_digits(self, data: list[int]) -> dict:
        """Count occurrences of each digit from 1 to 9 in the data"""
        digit_counts = {i: 0 for i in range(1, 10)}
        for number in data:
            first_digit = int(str(abs(number))[0])
            if 1 <= first_digit <= 9:
                digit_counts[first_digit] += 1
        return digit_counts

    def get_expected_percentages(self) -> dict:
        """Get the expected percentages according to Benford's Law"""
        expected = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        return {i: expected[i-1] for i in range(1, 10)}

    def get_p_value(self, data: list[int]) -> tuple:
        """Calculate p-value using chi-squared test"""
        observed_counts = self.count_digits(data)
        total_observed = sum(observed_counts.values())
        expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        expected_counts = [total_observed * prop for prop in expected_proportions]
        chi2_stat, p_value = chisquare(list(observed_counts.values()), expected_counts)
        return p_value, chi2_stat

    def get_ks_test(self, data: list[int]) -> tuple:
        """Perform the Kolmogorov-Smirnov test"""
        expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        total_observed = len(data)
        observed_counts = self.count_digits(data)
        observed_proportions = [observed_counts[digit] / total_observed for digit in range(1, 10)]
        cumulative_observed = np.cumsum(observed_proportions)
        cumulative_expected = np.cumsum(expected_proportions)
        ks_statistic = np.max(np.abs(cumulative_observed - cumulative_expected))
        ks_p_value = kstest(cumulative_observed, cumulative_expected)[1]
        return ks_statistic, ks_p_value

    def get_mad(self, data: list[int]) -> float:
        """Calculate the Mean Absolute Deviation (MAD)"""
        expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        total_observed = len(data)
        observed_counts = self.count_digits(data)
        observed_proportions = [observed_counts[digit] / total_observed for digit in range(1, 10)]
        absolute_deviations = [abs(o - e) for o, e in zip(observed_proportions, expected_proportions)]
        mad = sum(absolute_deviations) / len(absolute_deviations)
        return mad
