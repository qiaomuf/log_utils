#!/usr/bin/env python
import sys
from operator import add
'''
Column-wise printing average of integer values
'''

sum = []
count = 0
divide = 1
if len(sys.argv) > 1:
    divide = int(sys.argv[1])
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
print ' '.join(["%.2f"%(v) for v in [s/float(count * divide) for s in sum]])
