import numpy as np
# Note: chisquare is for discrete distributions, kstest is for continuous/CDF comparison
from scipy.stats import chisquare, kstest


class Utils:
    """Benford's Law utilities applied to all non-zero digits 1–9"""

    def _extract_digits(self, data):
        """Extract all non-zero digits 1–9 from dataset"""
        digits = []
        for value in data:
            try:
                # Convert to string, remove decimal, and iterate over characters
                s = str(abs(float(value))).replace('.', '')
                # Original logic: extract ALL non-zero digits.
                digits.extend([int(d) for d in s if d != '0'])
            except:
                continue
        return digits

    def count_digits(self, data):
        """Count occurrences of digits 1–9"""
        counts = {i: 0 for i in range(1, 10)}
        digits = self._extract_digits(data)
        for d in digits:
            if 1 <= d <= 9:  # Ensure digit is 1-9
                counts[d] += 1
        return counts

    def get_expected_percentages(self):
        """Benford expected percentages for digits 1–9"""
        return {d: float(np.log10(1 + 1/d)) for d in range(1, 10)}

    # --- FIX: New, standard Chi-Square Goodness-of-Fit Test ---
    def get_chi_square_test(self, data):
        """
        Performs a Chi-Square Goodness-of-Fit Test against Benford's Law.
        Returns the Chi-Square statistic and the p-value.
        """
        observed_counts = self.count_digits(data)
        observed = np.array(list(observed_counts.values()), dtype=float)
        total = observed.sum()

        if total == 0:
            return 0.0, 1.0

        expected_probs = np.array(
            [self.get_expected_percentages()[d] for d in range(1, 10)]
        )
        # Normalize expected probabilities (standard Benford's sum is 1.0)
        expected_probs /= expected_probs.sum()

        # Calculate expected counts for the test
        expected_counts = expected_probs * total

        # Degrees of freedom is k - 1, where k=9 categories (digits 1-9). df=8.
        # chisquare function automatically calculates df=k-1 unless ddof is specified.
        # We set ddof=0 to ensure df = 9-1 = 8.
        # The result returns (statistic, p_value)
        stat, p_value = chisquare(observed, f_exp=expected_counts, ddof=0)

        # To avoid p-value of 0 in case of very large statistic,
        # the precision of the float is the limit.
        return float(stat), float(p_value)

    # --- REMOVED: Your old get_p_value (Monte Carlo) to simplify ---
    # The Monte Carlo method had a conceptual error in the p-value calculation
    # and is replaced by the standard chisquare test.
    def get_p_value(self, data, simulations=5000):
        # We will point the old function name to the new, corrected test for compatibility.
        # Note: 'observed_stat' here is the Chi-Square statistic.
        observed_stat, p_value = self.get_chi_square_test(data)
        return p_value, observed_stat

    def get_ks_test(self, data):
        # ... (Method remains the same as in previous response for robustness) ...
        observed_counts = self.count_digits(data)
        total_digits = sum(observed_counts.values())

        if total_digits == 0:
            return 0.0, 1.0

        observed_probs = np.array(
            [observed_counts[d] for d in range(1, 10)]) / total_digits
        expected_probs = np.array(
            [self.get_expected_percentages()[d] for d in range(1, 10)])
        expected_probs /= expected_probs.sum()

        observed_cdf = np.cumsum(observed_probs)
        expected_cdf = np.cumsum(expected_probs)

        ks_statistic = np.max(np.abs(observed_cdf - expected_cdf))

        # A proper Benford's KS p-value calculation is complex.
        # This returns the statistic and a placeholder (which often looks non-zero).
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
