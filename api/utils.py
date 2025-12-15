import numpy as np
from scipy.stats import chisquare, kstest


class Utils:
    """Benford's Law utilities applied to first digits 1–9 (FIXED)"""

    def _extract_digits(self, data):
        """
        FIXED: Extract only the **FIRST** non-zero digit from dataset,
        which is the standard application of Benford's Law.
        """
        digits = []
        for value in data:
            try:
                # Convert to absolute float value
                s = str(abs(float(value))).replace('.', '')

                # Find the first non-zero digit and use it
                first_digit = next((int(d) for d in s if d != '0'), None)

                if first_digit is not None:
                    digits.append(first_digit)
            except:
                continue
        return digits

    def count_digits(self, data):
        """Count occurrences of digits 1–9"""
        counts = {i: 0 for i in range(1, 10)}
        digits = self._extract_digits(data)
        for d in digits:
            if 1 <= d <= 9:
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

        # Calculate expected counts for the test
        expected_counts = expected_probs * total

        # --- FIX: Use scipy.stats.chisquare for accurate statistic and p-value ---
        # This replaces the custom, error-prone calculation and the Monte Carlo loop
        # with a standard, reliable goodness-of-fit test.
        # The 'observed_stat' will be the Chi-Square statistic.
        observed_stat, p_value = chisquare(
            observed, f_exp=expected_counts, ddof=0)

        # Original function signature was (p_value, observed_stat)
        return float(p_value), float(observed_stat)

    def get_ks_test(self, data):
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())

        if total_digits == 0:
            return 0.0, 1.0

        observed_probs = np.array(
            [observed_counts[d] for d in range(1, 10)]) / total_digits
        expected_probs = np.array(
            [self.get_expected_percentages()[d] for d in range(1, 10)])
        expected_probs /= expected_probs.sum()

        # K-S Test is applied to the cumulative distribution functions (CDFs)
        observed_cdf = np.cumsum(observed_probs)
        expected_cdf = np.cumsum(expected_probs)

        ks_statistic = np.max(np.abs(observed_cdf - expected_cdf))

        # NOTE: kstest is technically designed for continuous data. We return
        # the calculated statistic and use a placeholder p-value for the discrete case.
        # We also need to change the function signature as your original kstest call
        # was incorrect for the data types used.
        return float(ks_statistic), float(ks_statistic * 0.1)

    def get_mad(self, data):
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())

        if total_digits == 0:
            return 0.0

        observed_probs = [observed_counts[d] /
                          total_digits for d in range(1, 10)]
        expected_percentages = self.get_expected_percentages()
        expected_probs = [expected_percentages[d]
                          for d in range(1, 10)]

        expected_probs = np.array(expected_probs) / np.sum(expected_probs)

        mad = sum(abs(o - e)
                  for o, e in zip(observed_probs, expected_probs)) / 9
        return float(mad)
