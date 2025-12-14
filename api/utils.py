import numpy as np
from scipy.stats import chisquare, kstest


class Utils:
    """All-digit (0–9) distribution utilities"""

    def _extract_digits(self, data):
        digits = []
        for value in data:
            for d in str(abs(int(value))):
                digits.append(int(d))
        return digits

    def count_digits(self, data):
        """Count occurrences of digits 0–9"""
        counts = {i: 0 for i in range(10)}
        digits = self._extract_digits(data)

        for d in digits:
            counts[d] += 1

        return counts

    def get_expected_percentages(self):
        """Uniform expected distribution for digits 0–9"""
        return {i: 0.10 for i in range(10)}

    def get_p_value(self, data):
        """Chi-square test against uniform distribution"""
        observed_counts = self.count_digits(data)
        observed = list(observed_counts.values())

        total = sum(observed)
        expected = [total * 0.10] * 10

        chi2_stat, p_value = chisquare(observed, expected)
        return p_value, chi2_stat

    def get_ks_test(self, data):
        observed_counts = self.count_digits(data)
        total = sum(observed_counts.values())

        observed_probs = np.array(
            [observed_counts[d] / total for d in range(10)]
        )
        expected_probs = np.array([0.10] * 10)

        ks_statistic = np.max(
            np.abs(np.cumsum(observed_probs) - np.cumsum(expected_probs))
        )

        ks_p_value = kstest(
            np.cumsum(observed_probs),
            np.cumsum(expected_probs)
        ).pvalue

        return ks_statistic, ks_p_value

    def get_mad(self, data):
        observed_counts = self.count_digits(data)
        total = sum(observed_counts.values())

        observed_probs = [
            observed_counts[d] / total for d in range(10)
        ]
        expected_probs = [0.10] * 10

        mad = sum(
            abs(o - e) for o, e in zip(observed_probs, expected_probs)
        ) / 10

        return mad
