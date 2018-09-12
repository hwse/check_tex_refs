import re
import argparse
import sys
import collections

class LabelCount:
    def __init__(self):
        self.label_nrs = list()
        self.ref_nrs = list()

    def label_found(self, line_nr):
        self.label_nrs.append(line_nr)

    def ref_found(self, line_nr):
        self.ref_nrs.append(line_nr)

def first(it):
    for el in it:
        if el:
            return el

def check_missing(file_name):
    with open(file_name, 'r') as file:
        counters = collections.defaultdict(lambda: LabelCount())
        label_re = r'\\label{(\w+)}|label\s*=\s*{?(\w+)}?'
        ref_re = r'\\ref{(\w+)}'
        
        for nr, line in enumerate(file.readlines()):
            # ignore comments
            if '%' in line: # TODO: only match on comments
                i = line.find('%') 
                line = line[:i]

            for id in map(first, re.findall(label_re, line)):
                counters[id].label_found(nr)
            for id in re.findall(ref_re, line):
                counters[id].ref_found(nr)
        print_errors(counters)

def print_errors(counters_dict):
    for id, count in counters_dict.items():
        if len(count.label_nrs) == 0:
            print('ref to {} has no matching label (lines: {})'.format(id, ','.join(map(str, count.label_nrs))))
        if len(count.ref_nrs) == 0:
            print('label {} was never referenced (lines: {})'.format(id, ','.join(map(str, count.label_nrs))))

def main():
    parser = argparse.ArgumentParser(description='Check a tex file for missing references to labels')
    parser.add_argument('file', help='path to the tex file that should be checked')
    args = parser.parse_args(sys.argv[1:])
    file = args.file
    check_missing(file)
    
if __name__ == '__main__':
    main()