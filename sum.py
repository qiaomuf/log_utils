#!/usr/bin/env python
import sys

for line in sys.stdin:
    print sum(int(v) for v in line.strip().split(' '))
