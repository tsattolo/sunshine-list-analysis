#!/usr/bin/env python3
"""
Add ID columns for Employers or Job Titles that will represent the category
each entry was put into in agg.py.
"""

import json
import sys
import pandas as pd
import pdb

from distances import *

def main():
    folder = sys.argv[1]
    col = sys.argv[2]
    df = pd.read_pickle(sys.argv[3])

    new_col = [0] * len(df)  #Those left at 0 are seconded sectors
    for d in range(n_sect):
        with open(folder + str(d) + col + 'Dict.json') as f:
            cdict = json.loads(f.read())
        
        line = df.loc[df['SectorID'] == d][col] 
        for i, r in line.items():
            for k, v in cdict.items():
                if r in [tuple(t[1]) for t in v]:
                    new_col[int(i)] = int(k) + 1       #Reserve 0 for seconded sectors
                    break
            else:
                print('Not found: ')
                print(r)


    print(len(new_col))
    new_col_name = col + 'ID'
    df[new_col_name] = new_col
                   
    df.to_pickle(sys.argv[4])

if __name__ == "__main__":
    main()
