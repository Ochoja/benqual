import numpy as np
from scipy.stats import chisquare, kstest


class Utils:
    """Benford's Law utilities applied to all digits (0–9)"""

    def _extract_digits(self, data):
        """Extract all digits (ignoring signs and decimal points)"""
        digits = []
        for value in data:
            try:
                s = str(abs(float(value))).replace(
                    '.', '')  # remove decimal point
                digits.extend([int(d) for d in s])
            except:
                continue
        return digits

    def count_digits(self, data):
        """Count occurrences of digits 0–9"""
        counts = {i: 0 for i in range(10)}
        digits = self._extract_digits(data)
        for d in digits:
            counts[d] += 1
        return counts

    def get_expected_percentages(self):
        """
        Expected Benford percentages for digits 1–9,
        with 0 assigned to normalize sum to 1
        """
        benford_probs = [np.log10(1 + 1/d) for d in range(1, 10)]
        prob_0 = 1 - sum(benford_probs)
        expected = [prob_0] + benford_probs
        return {i: float(expected[i]) for i in range(10)}

    def get_p_value(self, data):
        """Chi-square test against expected Benford percentages"""
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())

        expected_percentages = self.get_expected_percentages()
        expected = [expected_percentages[i] * total_digits for i in range(10)]

        # Normalize expected counts to exactly match sum of observed counts
        expected_sum = sum(expected)
        expected = [e * total_digits / expected_sum for e in expected]

        chi2_stat, p_value = chisquare(f_obs=list(
            observed_counts.values()), f_exp=expected)
        return float(p_value), float(chi2_stat)

    def get_ks_test(self, data):
        """Kolmogorov–Smirnov test"""
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())
        observed_probs = np.array(
            [observed_counts[i] / total_digits for i in range(10)])
        expected_probs = np.array(
            [self.get_expected_percentages()[i] for i in range(10)])
        ks_statistic = np.max(
            np.abs(np.cumsum(observed_probs) - np.cumsum(expected_probs)))
        ks_p_value = kstest(np.cumsum(observed_probs),
                            lambda x: np.cumsum(expected_probs)).pvalue
        return float(ks_statistic), float(ks_p_value)

    def get_mad(self, data):
        """Mean Absolute Deviation from expected percentages"""
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())
        observed_probs = [observed_counts[i] / total_digits for i in range(10)]
        expected_probs = [self.get_expected_percentages()[i]
                          for i in range(10)]
        mad = sum(abs(o - e)
                  for o, e in zip(observed_probs, expected_probs)) / 10
        return float(mad)
