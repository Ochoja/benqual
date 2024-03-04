"""Contains utilities for calculating benford Law"""
import pandas as pd


class Utils:
    """Checks the quality of data"""

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
        """Extract values from a column"""
        try:
            df = pd.read_csv(filename)  # loads file into dataframe
            values = pd.to_numeric(df[column], errors='coerce')
            return values.dropna().astype(int).tolist()
        except Exception as e:
            print("Error converting value", e)
            return None

    def compute_first_digit(self, number: int) -> int:
        """Compute first digit of number"""
        while number >= 10:
            number //= 10
        return number

    def extract_first_digits(self, data: list[int]) -> list:
        """Extract first digits of data set"""
        first_digits = [self.compute_first_digit(
            abs(number)) for number in data]
        return first_digits

    def count_digits(self, data: list[int]) -> dict:
        """Count number of digits from 1-9"""
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
                    digit_counts[digit] / total_digits) * 100, 2)

        return digit_percentages
