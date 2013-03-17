#!/usr/bin/env python

import sys
import math
import collections

'''
Print distributions of positive numbers. There should be one number per line.
The first argument can set TimeInterval.
The second arguemnt can set the max value of the time intervals.
'''

def naive_variance(data):
    n = 0
    Sum = 0
    Sum_sqr = 0
 
    for x in data:
        n = n + 1
        Sum = Sum + x
        Sum_sqr = Sum_sqr + x*x
 
    variance = (Sum_sqr - ((Sum*Sum)/n))/(n - 1)
    return variance

numbers = sorted(int(line) for line in sys.stdin if line.strip() if int(line) >= 0)

ratios = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
number_len = len(numbers)
for ratio in ratios:
    print "Top %-3d%%:\t"%(ratio * 100),
    number_part = numbers[int(number_len * (1 - ratio)):]
    print("average=%-10.2f\tmax=%-10d\tmin=%-10d\tstdev=%-10.2f\ttotal_num=%-10d"%(sum(number_part) / float(len(number_part)), max(number_part), min(number_part), math.sqrt(naive_variance(number_part)), len(number_part)))

end = numbers[-1]
if len(sys.argv) >= 2:
    span = int(sys.argv[1])
    if len(sys.argv) == 3:
        end = int(sys.argv[2])
else:
    span = max(numbers) / 15

number_contribution = collections.Counter()
number_distribution = collections.Counter()
for number in numbers:
    interval = min(number, end) / span
    number_contribution[interval] += number
    number_distribution[interval] += 1

# Printing...
keys = sorted(number_contribution.keys())
total_stars = 250
print 'Distribution'
for i in range(len(number_contribution)):
    distribution = number_distribution[keys[i]]
    print "%-7s %10.2f: %s"%(i * span, number_distribution[keys[i]],'*' * int(distribution * total_stars / float(len(numbers)) + 1))
print

print 'Contribution'
for i in range(len(number_contribution)):
    contribution = number_contribution[keys[i]] / float(sum(numbers))
    print "%-7s %10.2f%%: %s"%(i * span, contribution * 100, '*' * int(total_stars * contribution + 1))
print
