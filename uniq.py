#!/usr/bin/env python

import sys

if len(sys.argv) > 1 and sys.argv[1] == '-c':
    print len(set(l.strip() for l in sys.stdin.readlines()))

for line in set(l.strip() for l in sys.stdin.readlines()):
    if line:
        print line
