#!/usr/bin/env python
import sys
from operator import add
'''
Column-wise printing sum of integer values
'''

sum = []
for line in sys.stdin:
    try:
        items = [float(v) for v in line.strip().split()]
        if not items:
            continue
        if not sum:
            sum = items
        else:
            sum = map(add, sum, items)
        count += 1
    except:
        continue
print ' '.join(["%.2f"%s for s in sum])
