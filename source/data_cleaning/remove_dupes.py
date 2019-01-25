#!/usr/bin/env python3
"""
Find instances is which people.py decided that two or more entries from the 
same year are for the same person and correct this.
"""

import sys
import pandas as pd
import pdb
import time
import numpy as np
import math

from distances import *

def closeness(a, b):

    if a[N] == b[N]:
        return 1.0
    
    if a[LN] == b[LN]:
        if a[FN] == b[FN]:
            return 0.99
        elif a[FN] == []:
            if [s[0] for s in b[FN]] ==  a[FI]:
                return 0.98
        elif b[FN] == []:
            if [s[0] for s in a[FN]] ==  b[FI]:
                return 0.98

    return max(seqm(a[N],b[N]), jaccard(a[N], b[N]))

def main():
    df = pd.read_pickle(sys.argv[1])
    
    df = df.reset_index()
    del(df['index'])


    pidc = df['PrelimID']
    ids = sorted(set([e for e in pidc if not math.isnan(e)]))


    scnd_id = [None] * len(df)
    start_time = time.time()

    for i in ids:
        dfi = df[pidc == i]
        x = 0
        
        
        years = sorted(set(dfi[CY]))

        if i % 10000 == 0:
            print('%i: %f' % (i, time.time() - start_time))

        if len(years) == len(dfi):
            for j in dfi.index:
                scnd_id[j] = 0
            continue
            
        for y in years:
            dfyl = dfi[dfi[CY] == y - 1]
            dfy = dfi[dfi[CY] == y]
            if len(dfyl) == 0:
                for j in dfy.index:
                    scnd_id[j] = x
                    x += 1
            else:
                matches = []
                for j, r in dfy.iterrows():
                    for jl, rl in dfyl.iterrows():
                        matches.append((closeness(r, rl), -abs(r[S] - rl[S]),  j, jl))

                matches = sorted(matches, reverse=True)
                n = 0
                used = []
                for t in matches:
                    if scnd_id[t[2]] is None and t[3] not in used:
                        scnd_id[t[2]] = scnd_id[t[3]]
                        used.append(t[3])
                        n += 1
                    if n == len(dfy):
                        break
                else:
                    for t in matches:
                        if scnd_id[t[2]] is None:
                            scnd_id[t[2]] = x
                            x += 1



    real_id = [None] * len(df) 
    offset = 0
    for i in ids:
        dfi = df[pidc == i]
        if len(dfi) == 0:
            continue
        ms = 0
        for j, r in dfi.iterrows():
            real_id[j] = i + scnd_id[j] + offset
            ms = max(scnd_id[j], ms)

        offset += ms

    
    df['RealID'] = real_id
    df.to_pickle(sys.argv[2])
    

if __name__ == "__main__":
    main()

