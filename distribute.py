#!/usr/bin/env python

import sys
import math

from optparse import OptionParser

def print_stars(span, data, total, total_stars=100):
    keys = data.keys()
    keys.sort()
    for key in keys:
        num = data[key]
        print "%-7s %10.2f%% %s"%(key * span, num * 100/ float(total), '*' * int(num * total_stars / float(total) + 1))

def print_contribution(number_contribution, span):
    print_stars(span, number_contribution, sum(numbers))

def print_groups(groups):
    print_stars(1, groups, sum(groups.values()))

def print_accumulation(number_distribution, span):
    number_accumulation = {}
    keys = number_distribution.keys()
    keys.sort()
    number_accumulation[keys[0]] = number_distribution[keys[0]]
    for i in range(1, len(keys)):
        number_accumulation[keys[i]] = number_accumulation[keys[i - 1]] + number_distribution[keys[i]]
    print_stars(span, number_accumulation, max(number_accumulation.values()), total_stars=80)

def print_distribution(number_distribution, span, end):
    for number in numbers:
        interval = min(number, end) / span
        number_distribution.setdefault(interval, 0)
        number_distribution[interval] += 1
    print_stars(span, number_distribution, len(numbers))

def naive_variance(data):
    if len(data) == 1:
        return 0
    n = 0
    Sum = 0
    Sum_sqr = 0
 
    for x in data:
        n = n + 1
        Sum = Sum + x
        Sum_sqr = Sum_sqr + x*x
 
    variance = (Sum_sqr - ((Sum*Sum)/n))/(n - 1)
    return variance

def print_ratios(bottom):
    ratios = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 1]
    for ratio in ratios:
        if bottom:
            print "Bottom %-3d%%:\t"%(ratio * 100),
            number_part = numbers[:int(len(numbers) * ratio)]
        else:
            print "Top %-3d%%:\t"%(ratio * 100),
            number_part = numbers[int(len(numbers) * (1 - ratio)):]
        print("average=%-10.2f\tmax=%-10d\tmin=%-10d\tstdev=%-10.2f\ttotal_num=%-10d"% (sum(number_part) / float(len(number_part)),
                                                                                        max(number_part),
                                                                                        min(number_part),
                                                                                        math.sqrt(naive_variance(number_part)),
                                                                                        len(number_part)))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s', '--step', help='bin size', dest='span', type='int', default=-1)
    parser.add_option('-e', '--end', help='max column in the distribution', dest='end', type='int', default=-1)
    parser.add_option('-a', '--accumulate', help='accumulation', dest='use_accumulcation', action="store_true", default=False)
    parser.add_option('-c', '--contribution', help='calculate contribution', dest='use_contribution', action="store_true", default=False)
    parser.add_option('-g', '--group', help='group by first column', dest='use_group', action="store_true", default=False)
    parser.add_option('-b', '--bottom', help='Use bottom instead of top', dest='bottom', action="store_true", default=False)

    (options, args) = parser.parse_args()

    if not options.use_group:
        numbers = [float(line) for line in sys.stdin if line.strip() if float(line) >= 0]
        numbers.sort()
    else:
        pairs = [line.strip().split() for line in sys.stdin if line.strip()]
        numbers = []
        groups = {}
        for pair in pairs:
            t, n = pair[0], float(pair[1])
            if n >= 0:
                numbers.append(n)
                groups.setdefault(t, 0)
                groups[t] += n
        numbers.sort()

    if options.end == -1:
        options.end = numbers[-1]
    if options.span == -1:
        options.span = 100000

    if options.use_contribution:
        number_contribution = {}
        for number in numbers:
            interval = min(number, options.end) / options.span
            number_contribution.setdefault(interval, 0)
            number_contribution[interval] += number
        print_contribution(number_contribution, options.span)
        sys.exit(0)

    if options.use_group:
        print_groups(groups)
        sys.exit(0)

    # Distribution and Accumulation
    number_distribution = {}
    print_distribution(number_distribution, options.span, options.end)
    if options.use_accumulcation:
        print_accumulation(number_distribution, options.span)

    print_ratios(options.bottom)
