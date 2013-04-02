#!/usr/bin/env python
import sys
from optparse import OptionParser

field_value_separator = '='

fields_to_pick = [field for field in sys.argv[1:] if not field.startswith('-')]
opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]
parser = OptionParser()
parser.add_option('-t', '--time', dest="print_time", action="store_true", default=False)
parser.add_option('-p', '--pid', dest="print_pid", action="store_true", default=False)
(options, args) = parser.parse_args(opts)

try:
    file = open(fields_to_pick[-1])
    del fields_to_pick[-1]
except:
    file = sys.stdin

selected_count = 0
total_count = 0
for line in file:
    total_count += 1
    selected_fields = dict((field, 0) for field in fields_to_pick)
    items = line.strip().split()
    if options.print_time:
        curr_time = items[2][:5]
    if options.print_pid:
        if items[4].isdigit():
            pid = items[4]
        elif items[5].isdigit():
            pid = items[5]
        else:
            continue
    for item in items:
        field_string = item.split(field_value_separator)
        if field_string[0] in fields_to_pick and len(field_string) == 2:
            selected_fields[field_string[0]] = field_string[1]
    if not any(selected_fields.values()):
        continue
    fields_str = ' '.join(str(selected_fields[field]) for field in fields_to_pick)
    if options.print_time:
        print curr_time + ' ' + fields_str
    elif options.print_pid:
        print pid + ' ' + fields_str
    else:
        print fields_str
    selected_count += 1

if total_count and selected_count / float(total_count) < 0.90:
    sys.stderr.write("WARNING: only %d of %d lines are selected\n"%(selected_count, total_count))
