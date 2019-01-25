#!/usr/bin/env python3
"""
Remove punctuation from salaries to get float values.
"""
import pandas as pd
import time
import string
import re
import pdb
import sys

def main():
    infile = sys.argv[1]
    df = pd.read_pickle(infile)
    ss = df['Salary Paid']


    i = 0
    s_col = []
    for a in ss:
        if type(a) is not str:
            assert(type(a) is float)
        else:
            a = a.replace(',', '')
            a = a.replace('$', '')
            a = float(a)
        
        s_col.append(a)
       
    print(len(s_col))

    df['StrippedSalary'] = s_col

    outfile = sys.argv[2]
    df.to_pickle(outfile)

if __name__ == "__main__":
    main()
