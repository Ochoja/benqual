import pandas as pd
from scipy.stats import chisquare, kstest
import numpy as np

class Utils:
    """Benford's law Utility Functions"""

    # ... (existing methods) ...

    def get_ks_test(self, data: list[int]) -> tuple:
        """Perform the Kolmogorov-Smirnov test"""
        # Benford's Law expected proportions for digits 1 to 9
        expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

        # Calculate total observed digits
        total_observed = len(data)

        # Calculate observed proportions
        observed_counts = self.count_digits(data)
        observed_proportions = [observed_counts[digit] / total_observed for digit in range(1, 10)]

        # Calculate cumulative observed and expected proportions
        cumulative_observed = np.cumsum(observed_proportions)
        cumulative_expected = np.cumsum(expected_proportions)

        # Calculate the Kolmogorov-Smirnov statistic and p-value
        ks_statistic = np.max(np.abs(cumulative_observed - cumulative_expected))
        ks_p_value = kstest(cumulative_observed, cumulative_expected)[1]

        return ks_statistic, ks_p_value

    def get_mad(self, data: list[int]) -> float:
        """Calculate the Mean Absolute Deviation (MAD)"""
        # Benford's Law expected proportions for digits 1 to 9
        expected_proportions = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

        # Calculate total observed digits
        total_observed = len(data)

        # Calculate observed proportions
        observed_counts = self.count_digits(data)
        observed_proportions = [observed_counts[digit] / total_observed for digit in range(1, 10)]

        # Calculate the absolute deviations
        absolute_deviations = [abs(o - e) for o, e in zip(observed_proportions, expected_proportions)]

        # Calculate the Mean Absolute Deviation (MAD)
        mad = sum(absolute_deviations) / len(absolute_deviations)

        return mad
