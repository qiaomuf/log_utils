#!/usr/bin/env python
import sys
from optparse import OptionParser

field_value_separator = '='

fields_to_pick = [field for field in sys.argv[1:] if not field.startswith('-')]
opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]
parser = OptionParser()
parser.add_option('-t', '--time', dest="print_time", action="store_true", default=False)
parser.add_option('-p', '--pid', dest="print_pid", action="store_true", default=False)
parser.add_option('-q', '--query', dest="print_query", action="store_true", default=False)
parser.add_option('-s', '--source', dest="print_source", action="store_true", default=False)
parser.add_option('-d', '--print_default', dest="print_default", action="store_true", default=False)
parser.add_option('-f', '--qid_file', dest="qid_file", action="store", type='string', default='')
parser.add_option('-i', '--if', dest="if_cond", action="store", type='string', default='')
(options, args) = parser.parse_args(opts)

if options.qid_file:
    qids = {}
    qid_file = open(options.qid_file)
    for line in qid_file:
        qids[line.strip()] = 1

file_name = None
try:
    file = open(fields_to_pick[-1])
    file_name = fields_to_pick[-1]
    del fields_to_pick[-1]
except:
    file = sys.stdin

def any(values):
    for v in values:
        if v:
            return True
    return False

selected_count = 0
total_count = 0
for line in file:
    total_count += 1
    if options.print_query:
        import re
        group = re.search('\[.+\]', line)
        if group:
            query = group.group(0)
        else:
            continue
    items = line.strip().split()
    selected_fields = dict([(field, 0) for field in fields_to_pick])
    if options.print_time:
        try:
            curr_time = items[2][:]
        except:
            curr_time = ''
    if options.print_pid:
        if items[4].isdigit():
            pid = items[4]
        elif items[5].isdigit():
            pid = items[5]
        else:
            continue
    qid = ''
    for item in items:
        field_string = item.split(field_value_separator)
        if field_string[0] in fields_to_pick and len(field_string) == 2:
            selected_fields[field_string[0]] = field_string[1]
        if (field_string[0] == 'id' or field_string[0] == 'qid') and len(field_string) == 2:
            qid = field_string[1]
    if not any(selected_fields.values()) and not options.print_query and not options.print_default:
        continue
    if options.if_cond:
        if not eval(options.if_cond):
            continue
    fields_str = ' '.join([str(selected_fields[field]) for field in fields_to_pick])
    if options.print_time:
        fields_str = curr_time + ' ' + fields_str
    if options.print_pid:
        fields_str = pid + ' ' + fields_str
    if options.print_query:
        fields_str = query + ' ' + fields_str
    if options.qid_file:
        if not qid or qid not in qids:
            continue
    if options.print_source:
        fields_str = file_name + ' ' + fields_str
    print fields_str
    selected_count += 1

if total_count and selected_count / float(total_count) < 0.90:
    sys.stderr.write("WARNING: only %d of %d lines are selected\n"%(selected_count, total_count))
