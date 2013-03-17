#!/usr/bin/env python

'''
Compare two columns
'''

import sys
count = 0
total = 0
for line in sys.stdin:
    numbers = line.strip().split(' ')
    if numbers[0] > numbers[1]:
        count += 1
    total += 1
print count / float(total)
