import numpy as np
from scipy.stats import chisquare, kstest


class Utils:
    """Benford's Law utilities applied to all digits (0–9)"""

    def _extract_digits(self, data):
        """Extract all digits from integer and fractional parts of numbers"""
        digits = []
        for value in data:
            try:
                # Convert to string, remove non-digit chars (like '.','-')
                s = str(abs(float(value)))
                for c in s:
                    if c.isdigit():
                        digits.append(int(c))
            except:
                continue
        return digits

    def count_digits(self, data):
        counts = {i: 0 for i in range(10)}
        digits = self._extract_digits(data)
        for d in digits:
            counts[d] += 1
        return counts

    def get_expected_percentages(self):
        """Benford expected percentages for digits 0-9"""
        benford_probs = [np.log10(1 + 1/d) for d in range(1, 10)]
        prob_0 = max(0, 1 - sum(benford_probs))  # ensure non-negative
        expected = [prob_0] + benford_probs
        return {i: float(expected[i]) for i in range(10)}

    def get_p_value(self, data):
        """Chi-square test with all expected counts > 0"""
        observed_counts = self.count_digits(data)
        observed = list(observed_counts.values())
        total = sum(observed)

        expected_percentages = self.get_expected_percentages()
        expected = [expected_percentages[i] * total for i in range(10)]

        # Ensure no zeros in expected counts (small datasets)
        expected = [max(e, 1e-6) for e in expected]

        chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
        return float(p_value), float(chi2_stat)

    def get_ks_test(self, data):
        """Kolmogorov–Smirnov test"""
        observed_counts = self.count_digits(data)
        total = sum(observed_counts.values())
        observed_probs = np.array(
            [observed_counts[i] / total for i in range(10)])
        expected_probs = np.array(
            [self.get_expected_percentages()[i] for i in range(10)])
        ks_statistic = np.max(
            np.abs(np.cumsum(observed_probs) - np.cumsum(expected_probs)))
        ks_p_value = kstest(np.cumsum(observed_probs),
                            lambda x: np.cumsum(expected_probs)).pvalue
        return ks_statistic, ks_p_value

    def get_mad(self, data):
        """Mean Absolute Deviation from expected percentages"""
        observed_counts = self.count_digits(data)
        total = sum(observed_counts.values())
        observed_probs = [observed_counts[i] / total for i in range(10)]
        expected_probs = [self.get_expected_percentages()[i]
                          for i in range(10)]
        mad = sum(abs(o - e)
                  for o, e in zip(observed_probs, expected_probs)) / 10
        return mad
