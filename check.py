import re
import argparse
import sys

class LabelCount:
    def __init__(self, labels=0, refs=0):
        self.labels = labels
        self.refs = refs

    def inc_labels(self):
        self.labels += 1

    def inc_refs(self):
        self.refs += 1


class LabelCounter:
    def __init__(self):
        self.counts = dict() # dict[id -> LabelCount]

    def label_found(self, id):
        if id in self.counts:
            self.counts[id].inc_labels()
        else:
            self.counts[id] = LabelCount(labels=1)

    def ref_found(self, id):
        if id in self.counts:
            self.counts[id].inc_refs()
        else:
            self.counts[id] = LabelCount(refs=1)

    def print_result(self):
        for id, count in self.counts.items():
            if count.labels == 0 and count.refs == 0:
                print('ERRRRROOORR')
            if count.labels == 0:
                print('ref to {} has no matching label'.format(id))
            if count.refs == 0:
                print('label {} was never referenced'.format(id))

def first(it):
    for el in it:
        if el:
            return el

def check_missing(file_name):
    with open(file_name, 'r') as file:
        lc = LabelCounter()
        label_re = r'\\label{(\w+)}|label\s*=\s*{?(\w+)}?'
        ref_re = r'\\ref{(\w+)}'
        for nr, line in enumerate(file.readlines()):
            if '%' in line:
                i = line.find('%')
                line = line[:i]
            # print(line)
            for label in map(first, re.findall(label_re, line)):
                # print(label)
                lc.label_found(label)
            for ref in re.findall(ref_re, line):
                # print(ref)
                lc.ref_found(ref)
        lc.print_result()
        

def main():
    parser = argparse.ArgumentParser(description='Check a tex file for missing references to labels')
    parser.add_argument('file', help='path to the tex file that should be checked')
    args = parser.parse_args(sys.argv[1:])
    file = args.file
    check_missing(file)
    
if __name__ == '__main__':
    main()