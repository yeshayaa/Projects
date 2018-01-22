import os
import sys
import csv
import random

from collections import OrderedDict

from numpy import mean, var, std
from numpy.random import randint
from scipy.stats import kurtosis

from itertools import combinations

# Names of csv files to read. This is a first pass. These files should
# be in their own inFiles directory. Any csv file can be read from there.
csv_name = 'doctor-attributes.csv'
csv_name2 = 'training.csv'
in_files = [csv_name, csv_name2]

# An list of csv files that have been read and parsed.
doc_attrs = []

"""
This is a rules base program. It is open-ended. It is possible to add new rules. Each one
executes a unique case. For the time being, each case is by the command. In the future, as 
more cases are added, cases can be have additional rules that are more complex.
. But for now, it took a very short time to add new cases.
"""

cases = [
    {'variables': [('adoption date', [1,2,3,4]), #1
                   ('med_sch_yr', [1, 2, 3, 4, 5, 6, 9])],
     'command': 'perms of v1 and v2',
     'title': 'analyze 2-dimensions if doctor age and relationship of review medical literature is relevant?'},

    {'variables': [('adoption date', [1,2,3,4]), #2
                   ('specialty', [1,2,3,4,9])],
     'command': 'perms of v1 and v2',
     'title': 'do a certain specialty adopt Safsprin?'},

    {'variables': [('adoption date', [1,2,3,4]), ('meetings', [0,1,2,9])], #3
     'command': 'perms of v1 and v2',
     'title': 'do doctors learn about Safsprin through meetings?'}, 

    {'variables': [('adoption date', [1,2,3,4]), ('jours', [1,2,3,4,5,6,7,8,9])], #4
     'command': 'perms of v1 and v2',
     'title': 'do adoption rate relate to journal articles?'},

    {'variables': [('adoption date', [1,2,3,4]), ('patients', [1,2,3,4,5,6])], #5
     'command': 'perms of v1 and v2',
     'title': 'do amount of patients see relate to adoption rate?'},

    {'variables': [('adoption date', [1,2,3,4]), ('city', [1,2,3,4])], #6
     'command': 'perms of v1 and v2',
     'title': 'do city have an effect on adoption rate of Safsprin?'},

    {'variables': [('adoption date', [1,2,3,4]), ('med_sch_yr', [1,2,3,4,5,6,9]), #7
                   ('specialty', [1,2,3,4,9])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'do med school year effect and specialty relate'},

    {'variables': [('adoption date', [1,2,3,4]), ('med_sch_yr', [1,2,3,4,5,6,9]), #8
                   ('jours', [1,2,3,4,5,6,7,8, 9])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'do med school year effect journal articles and adoption'}, 
    
    {'variables': [('adoption date',[1,2,3,4]), ('specialty', [1,2,3,4,9]), #9
                   ('jours', [1,2,3,4,5,6,7,8,9])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'specialty and journals with varibles'},

    {'variables': [('adoption date', [1,2,3,4]), ('specialty', [1,2,3,4,9]), #10
                   ('patients', [1,2,3,4,5,6])],
     'command': 'perms of v1 and v2 and v3', 
     'title': 'do specialty and patients relate with adoption rate?'},

    {'variables': [('adoption date', [1,2,3,4]), ('specialty', [1,2,3,4,9]), #11
                   ('city', [1,2,3,4])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'specialty and relationship with adoption rate'},

    {'variables': [('adoption date', [1,2,3,4]), ('specialty', [1,2,3,4,9])], #12
     'command': 'perms of v1 and v2',
     'title': 'do specialty and meetings and adoption rate relate?'},

    {'variables': [('adoption date', [1,2,3,4]), ('city', [1,2,3,4]), #13
                   ('patients', [1,2,3,4,5,6])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'do city and adoption date efect patients?'},

    {'variables': [('adoption date', [1,2,3,4]), ('jours', [1,2,3,4,5,6,7,8,9]), #14
                   ('meetings', [0,1,2,3,4])],
     'command': 'perms of v1 and v2 and v3',
     'title': 'do adoption rate and journal, and meetings relate?'},

    {'variables': [('adoption date', [1,2,3,4]), ('specialty', [1,2,3,4,9]), #15
                   ('jours', [1,2,3,4,5,6,7,8,9]), ('meetings', [0,1,2,3,4])],
     'command': 'perms of v1 and v2 and v3 and v4',
     'title': 'do adoption rate and specialty, journals, meetings all relate?'},

    {'variables': [('adoption date', [1,2,3,4]), ('city', [1,2,3,4]), #16
                   ('jours', [1,2,3,4,5,6,7,8,9]), ('meetings', [0,1,2,3,4])], 
     'command': 'perms of v1 and v2 and v3 and v3', 
     'title': 'do adoption rate, city, journals, and meetings relate?'},
]
     
def convert(reader):
    """Convert string fields to integer.

    Returns a list of dicts.
    """
    recs = []
    for record in reader:
        for k in record.keys():
            # Convert strings to integers (except the doctor's name)
            if k != 'doctor':
                record[k] =  int(record[k])
        recs.append(record)
    return recs

def write_stats(stuff):
    print( 'mean %f' %  mean(stuff))
    print( 'var %f' % var(stuff))
    print( 'std %f' % std(stuff))
    print( 'kurtosis %f' % kurtosis(stuff))
    print('\n')

class MakeWriter:
    """A csv writer.
    File name is the case number.
    """
    def __init__(self, idx, proto):
        if isinstance(idx, int):
            file_str = 'case%d.csv' % idx
        else:
            file_str = 'case%s.csv' % idx
        self.fd = open(file_str, 'w')
        self.writer = csv.DictWriter(self.fd, proto)
        self.writer.writeheader()

    def close(self):
        self.fd.flush()
        self.fd.close()

    def writerow(self, row):
        self.writer.writerow(row)

def two_way(tt):
    return [(a,b) for a in tt[0] for b in tt[1]]

def three_way(tt):
    return [(a,b,c) for a in tt[0] for b in tt[1] for c in tt[2]]

def four_way(tt):
    return [(a,b,c,d) for a in tt[0] for b in tt[1] for c in tt[2] for d in tt[3]]

def compute_perms(tt):
    funcs = [two_way, three_way, four_way]
    idx = len(tt) - 2
    if not idx >= 0 and idx < len(funcs):
        print('Number of arrays of values to permute is out of range')
        sys.exit()
    return funcs[idx](tt)

def split_keys_vals(xx):
    KEY = 0
    VAL = 1
    
    keys = [a[KEY] for a in xx]
    vals = [a[VAL] for a in xx]
    return keys, vals

def make_proto(keys):
    bb = [key for key in keys]
    bb.append('count')
    return bb

def calc_answer(doc, perm, keys):
    """All permutations are ANDED
    """
    ans = True
    for idx, key in enumerate(keys):
        if doc[key] != perm[idx]:
            ans = False
            break
    return ans

def calc_prob_cases(doc_attr):
    """calculate probability by case
    
    For each case, calculate the conditional probability according
    to the case's command.

    Note: all cases have similarities that can be refactored into similar functions.
    """
    for idx, case in enumerate(cases):
        answers = []

        if case['command'] == 'perms of v1 and v2' or \
           case['command'] == 'perms of v1 and v2 and v3' or \
           case['command'] == 'perms of v1 and v2 and v3 and v4':

            keys, vals = split_keys_vals(case['variables'])
            proto = make_proto(keys)
            print(proto)
            writer = MakeWriter(idx, proto)
            perms = compute_perms(vals)

            for doc in doc_attr:
                ans = 0
                for perm in perms:
                    if calc_answer(doc, perm, keys):
                        ans += 1
                line = {'count': ans}
                for idx, key in enumerate(keys):
                    line[key] = perm[idx]
                answers.append(ans)
                print (line)
                writer.writerow(line)
            write_stats(answers)
            writer.close()


        elif case['command'] == 'comb then perm of v1 or v2 and v3':
            combs = list(combinations(case['variables'][0][1], 2))
            perms = []
            for comb in combs:
                for val in case['variables'][1][1]:
                    perms.append((comb[0], comb[1], val))

            key1 = case['variables'][0][0]
            key2 = case['variables'][1][0]
            key1a = 'key%da' % 1
            key1b = 'key%da' % 2
            proto = (key1a, key1b, key2, 'count')
            writer = MakeWriter(idx, proto)        
            for val1, val2, val3 in perms:

                found = [True for doc in doc_attr if doc[key1] == val1 or \
                         doc[key1] == val2 and doc[key2] == val3]
                line = {key1a: val1, key1b: val2, key2: val3, 'count': len(found)}
                answers.append(len(found))
                print(line)
                writer.writerow(line)            
            write_stats(answers)
            writer.close()


## Read in comma separated doctor attributes. Each element is a dict.
for in_file in in_files:
    try:
        rdr = csv.DictReader(open(csv_name, 'r'), delimiter=',')
    except:
        print('%s cannot be opened. Exiting' % csv_name)
        sys.exit()
    doc_attrs.append(convert(rdr))
    

for doc_attr in doc_attrs:
    calc_prob_cases(doc_attr)
