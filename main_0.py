#!/usr/bin/env python3
from api.utils import Utils

Utils = Utils()

nums = Utils.extract_csv_values("uploads/test.csv", "Test_3")
print(nums)
