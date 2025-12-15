import numpy as np
from scipy.stats import chisquare, kstest


class Utils:
    """Benford's Law utilities applied to first digits 1–9"""

    def _extract_digits(self, data):
        """Extract only digits 1–9 from dataset"""
        digits = []
        for value in data:
            try:
                s = str(abs(float(value))).replace('.', '')
                digits.extend([int(d) for d in s if d != '0'])
            except:
                continue
        return digits

    def count_digits(self, data):
        """Count occurrences of digits 1–9"""
        counts = {i: 0 for i in range(1, 10)}
        digits = self._extract_digits(data)
        for d in digits:
            if d != 0:
                counts[d] += 1
        return counts

    def get_expected_percentages(self):
        """Benford expected percentages for digits 1–9"""
        return {d: float(np.log10(1 + 1/d)) for d in range(1, 10)}

    def get_p_value(self, data):
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())
        expected_percentages = self.get_expected_percentages()
        expected = [expected_percentages[d] *
                    total_digits for d in range(1, 10)]
        chi2_stat, p_value = chisquare(f_obs=list(
            observed_counts.values()), f_exp=expected)
        return float(p_value), float(chi2_stat)

    def get_ks_test(self, data):
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())
        observed_probs = np.array(
            [observed_counts[d]/total_digits for d in range(1, 10)])
        expected_probs = np.array(
            [self.get_expected_percentages()[d] for d in range(1, 10)])
        ks_statistic = np.max(
            np.abs(np.cumsum(observed_probs) - np.cumsum(expected_probs)))
        ks_p_value = kstest(np.cumsum(observed_probs),
                            lambda x: np.cumsum(expected_probs)).pvalue
        return float(ks_statistic), float(ks_p_value)

    def get_mad(self, data):
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())
        observed_probs = [observed_counts[d] /
                          total_digits for d in range(1, 10)]
        expected_probs = [self.get_expected_percentages()[d]
                          for d in range(1, 10)]
        mad = sum(abs(o - e)
                  for o, e in zip(observed_probs, expected_probs)) / 9
        return float(mad)
