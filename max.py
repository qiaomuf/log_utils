#!/usr/bin/env python
import sys
from operator import add
'''
Column-wise printing max integer values
'''

max_values = []
count = 0
for line in sys.stdin:
    items = [int(v) for v in line.strip().split()]
    if not max_values:
        max_values = items
    else:
        max_values = map(max, max_values, items)
if max_values:
    print ' '.join(str(v) for v in max_values)
