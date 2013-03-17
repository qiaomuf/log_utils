#!/usr/bin/env python
import sys

fields_separator = ' '
field_value_separator = '='

if sys.argv[-1] == '-':
    file = sys.stdin
else:
    file = open(sys.argv[-1])

fields_to_pick = sys.argv[1:-1]
selected_count = 0
total_count = 0
for line in file:
    total_count += 1
    selected_fields = dict((field, '0') for field in fields_to_pick)
    items = line.strip().split(fields_separator)
    for item in items:
        field_string = item.split(field_value_separator)
        if field_string[0] in fields_to_pick and len(field_string) == 2:
            selected_fields[field_string[0]] = field_string[1]
    if not any(selected_fields):
        continue
    print ' '.join(selected_fields[field] for field in fields_to_pick)
    selected_count += 1

if total_count and selected_count / float(total_count) < 0.90:
    sys.stderr.write("WARNING: only %d of %d lines are selected\n"%(selected_count, total_count))
