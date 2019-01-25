#!/usr/bin/env python3
"""
Reorganize dataframe to have one row per person and one columns for each years salary.
"""
import sys
import pandas as pd
import pdb
import time

from distances import *

def main(): 
    df = pd.read_pickle('./' + sys.argv[1])
    
    df_out = pd.DataFrame()
    
    rid = df['RealID']

    start_time = time.time()
    for i in range(1, int(max(rid)) + 1):
        dfi = df[rid == i]
        if len(dfi) == 0:
            continue
        
        years = range(1996,2018)
        dfa = dfi.head(1).copy()
        sals = []
        for y in years:
            sal = 0.0
            tb = 0.0
            if y in list(dfi[CY]):
                r = dfi[dfi[CY] == y].squeeze()
                sal = r['StrippedSalary']
                tb = str(r['Taxable Benefits'])
                 
                tb = tb.replace(',', '')
                tb = tb.replace('$', '')
                try:
                    tb = float(tb)
                except ValueError:
                    tb = 0.0

            dfa['Benefits' + str(y)] = tb
            dfa['Salary' + str(y)] = sal
            sals.append(sal)

        #if not any(sals):
        #    print(sals)
        #    pdb.set_trace()

        dfa['RealID'] = i
        df_out = df_out.append(dfa, ignore_index=True)

        if i % 1000 == 0:
            print('%i: %f' % (i, time.time() - start_time))

    df_out.to_pickle(sys.argv[2])
        



if __name__ == "__main__":
    main()
