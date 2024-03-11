#!/usr/bin/env python3
from api.utils import Utils

Utils = Utils()

digits = Utils.get_number_pool([45, 55])
print(digits)
