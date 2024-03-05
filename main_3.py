#!/usr/bin/env python3
from api.utils import Utils

Utils = Utils()

nums = Utils.extract_csv_values("uploads/test.csv", "Test")
first_digits = Utils.extract_first_digits(nums)

print(first_digits)
print(Utils.count_digits(first_digits))
print(Utils.get_digit_percentages(first_digits))
print(Utils.get_p_value(first_digits))
