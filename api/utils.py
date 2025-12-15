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

    def get_p_value(self, data, simulations=5000):
        observed_counts = self.count_digits(data)
        observed = np.array(list(observed_counts.values()), dtype=float)
        total = observed.sum()

        if total == 0:
            return 1.0, 0.0

        expected_probs = np.array(
            [self.get_expected_percentages()[d] for d in range(1, 10)]
        )
        expected_probs /= expected_probs.sum()

        # Observed statistic (chi-square style)
        observed_probs = observed / total
        observed_stat = np.sum(
            (observed_probs - expected_probs) ** 2 / expected_probs
        )

        # Monte Carlo distribution
        simulated_stats = np.zeros(simulations)
        for i in range(simulations):
            simulated = np.random.multinomial(int(total), expected_probs)
            sim_probs = simulated / total
            simulated_stats[i] = np.sum(
                (sim_probs - expected_probs) ** 2 / expected_probs
            )

        # Percentile-based p-value (FIX)
        percentile = np.mean(simulated_stats <= observed_stat)
        p_value = 1 - abs(percentile - 0.5) * 2

        return float(p_value), float(observed_stat)

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
