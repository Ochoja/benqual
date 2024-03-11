#!/usr/bin/env python3
from api.utils import Utils

Utils = Utils()

digits = Utils.extract_first_digits(['45', '55'])
print(digits)
