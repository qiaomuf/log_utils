#!/usr/bin/env python
import sys
from operator import add
'''
Column-wise printing average of integer values
'''

sum = []
count = 0
for line in sys.stdin:
    items = [int(v) for v in line.strip().split()]
    if not sum:
        sum = items
    else:
        sum = map(add, sum, items)
    count += 1
print ' '.join(str(v) for v in [s/float(count) for s in sum])
