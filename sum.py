#!/usr/bin/env python
import sys

for line in sys.stdin:
    print sum(float(v) for v in line.strip().split(' '))
