#!/usr/bin/env python

import sys
import re
import json

# delimiters for regular expression split. Includes white space.


class TextCount:
    """Put tile here.
    Put description here.
    """
    delims = '''\.|:|;|,|$|!|\s|"|\?|\n|-'''
    
    def __init__(self, infile):
        self.word_count = {}
        lines = open(infile, 'r').readlines()

        buff = []
        for line in lines:
            buff.extend(re.split(self.delims, line))

        for word in buff:
            if word and word != '\n':
                val = self.word_count.setdefault(word, 0)
                self.word_count[word] += 1

        # convert to a list so it can be sorted
        self.wc_sorted = [(key, val) for key, val in self.word_count.items()]
        self.wc_sorted = sorted(self.wc_sorted, key=lambda x: x[1], reverse=True)

    def t_print(self):
        for key, val in self.wc_sorted:
            print('%s -  %d' % (key, val))


    def j_print(self):
        json_buff = json.dumps(self.wc_sorted)
        print(json_buff)
            

if __name__ == '__main__':
    Usage = """Usage: python text_count.py text_file format=[text|json]"""

    if len(sys.argv) != 3:
        print(Usage)
        sys.exit()

    txt_file = sys.argv[1]
    c =  TextCount(txt_file)

    format = sys.argv[2].split('=')[1]
    if format == 'text':
        c.t_print()
    elif format == 'json':
        c.j_print()
    else:
        print('unknown print format: %s" % format')
        print(Usage)


