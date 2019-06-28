#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line_s = line.strip().split('\t')
    if len(line_s) > 6:
        line_s[5] = '|'.join(sorted(line_s[5].split('|'), key=lambda s: s.lower()))
        print('\t'.join(line_s))
    else:
        print(line, end="")
