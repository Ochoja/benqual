"""Contains utilities for calculating benford Law"""
import pandas as pd
from scipy.stats import chisquare


class Utils:
    """Benford's law Utility Functions"""

    def check_dataSet(self, data: list[str | int | float]) -> bool:
        """Check if data contains numbers only"""
        if not data:
            return False  # return false if list is empty or None
        else:
            for item in data:
                try:
                    val = int(item)
                    if type(val) is not int:
                        return False
                except Exception as e:
                    return False
        return True  # return true if all items pass test

    def extract_csv_values(self, filename: str, column: str) -> list:
        """Extract values from a column
            Save only number values"""
        try:
            df = pd.read_csv(filename)  # loads file into dataframe
            values = pd.to_numeric(df[column], errors='coerce')
            return values.dropna().astype(int).tolist()
        except Exception as e:
            print("Error converting value", e)
            return None

    def compute_first_digit(self, number: int | float) -> int:
        """Compute first digit of number"""
        if type(number) == float:
            number_str = str(abs(number))
            decimal_index = number_str.find('.')
            if decimal_index != -1:
                number_str = number_str[:decimal_index]
                return int(number_str[0])
        else:
            while number >= 10:
                number //= 10
            return number

    def extract_first_digits(self, data: list[int]) -> list:
        """Extract first digits of data set"""
        first_digits = [self.compute_first_digit(
            abs(number)) for number in data]
        return first_digits

    def count_digits(self, data: list[int]) -> dict:
        """Count number of occurences
            of digits from 1-9"""
        digit_counts = {i: 0 for i in range(1, 10)}
        for number in data:
            if number in digit_counts:
                digit_counts[number] += 1
        return digit_counts

    def get_digit_percentages(self, data: list[int]) -> dict:
        """Get percentages of numbers"""
        total_digits = len(data)
        digit_percentages = {i: 0 for i in range(1, 10)}
        digit_counts = self.count_digits(data)

        for digit in digit_counts.keys():
            if digit_counts[digit]:
                digit_percentages[digit] = round((
                    digit_counts[digit] / total_digits) * 100, 3)

        return digit_percentages

    def get_expected_percentages(self) -> dict:
        """Get Expected percentage based on Benford Law"""
        return {1: 30.1, 2: 17.6, 3: 12.5, 4: 9.7, 5: 7.9, 6: 6.7, 7: 5.8, 8: 5.1, 9: 4.6}

    def get_p_value(self, data: list[int]) -> float:
        """Get p-value and perform chi-square test"""
        expected_percentages = [30.1, 17.6, 12.5,
                                9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        observed_percentages = self.get_digit_percentages(data)

        total_expected_percentage = sum(expected_percentages)
        total_observed_percentage = sum(observed_percentages.values())

        # Adjust observed percentages to match the total sum of expected percentages
        for digit in observed_percentages:
            observed_percentages[digit] *= total_expected_percentage / \
                total_observed_percentage

        # perform the chi-square test
        chi2_stat, p_value = chisquare(
            list(observed_percentages.values()), f_exp=expected_percentages)

        return p_value
