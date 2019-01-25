#!/usr/bin/env python3
"""
Find entries in different years that correspond to the same person.
This is done by looking for matching names in the lists from future years
that were matched to the same Employer or Job Title.
This process may decide that two or more entries from the same year are for 
the same person. This is impossible and is corrected in remove_dupes.py.
"""

import sys
import pandas as pd
import pdb
import time
from distances import *

name_cols = [TL, FI, FN, MI, LN] 

last_resort = 0

def closeness(a, b, optim):

    if a[N] == b[N]:
        return 1.0, 2
    
    if optim == 1:
        return 0.0, 1

    if a[LN] == b[LN]:
        if a[FN] == b[FN]:
            return 0.99, 0
        elif a[FN] == []:
            if [s[0] for s in b[FN]] ==  a[FI]:
                return 0.98, 0
        elif b[FN] == []:
            if [s[0] for s in a[FN]] ==  b[FI]:
                return 0.98, 0

    
    return 0.0, 1

    

def get_matches(df, at_ind):
    matches = []
    strengths = []
    thresh = 0.85

    optim = 0
    for i, r in df.iterrows():
        strength, optim = closeness(r, at_ind, optim)
        if strength >= thresh:
            strengths.append(strength)
            matches.append(int(i))

    if not matches:
        for i, r in df.iterrows():
            strength = max(seqm(r[N], at_ind[N]), jaccard(r[N], at_ind[N]))
            if strength >= thresh:
                strengths.append(strength)
                matches.append(int(i))
    return (matches, strengths)
    
def main():
    df_orig = pd.read_pickle(sys.argv[1])
    all_years = len(sys.argv) >= 4 and sys.argv[3] == '-A'

    
    df_orig = df_orig.reset_index()
    del(df_orig['index'])

    df_out = df_orig

    print(all_years)

    filter_columns = ['StrippedEmpID', 'StrippedJobID']
    
    df = df_orig[[CY, 'StrippedSalary', 'SectorID', N] + filter_columns + name_cols]

    pers_id = [None]  * len(df)
   
    x = 1
    for i in df.loc[df[CY] == start_year].index:
        pers_id[int(i)] = int(x)
        x += 1

    start_time = time.time()
    total_row = x
    for sect in range(n_sect):  #12 sectors not including seconded 
        dfs = df[df['SectorID'] == sect]
        for y in range(start_year, start_year + n_years - 1):
            year_df = dfs[dfs[CY] == y + 1]
            prey_df = dfs[dfs[CY] == y] if not all_years else dfs[dfs[CY] <= y]
            for istr in year_df.index:
                i = int(istr)
                at_ind = df.loc[istr] 
                for n in range(len(filter_columns)):

                    cols = filter_columns[0:len(filter_columns)-n]
                    filt_df = prey_df[(prey_df[cols] == at_ind[cols]).all(axis='columns')]

                    matches, strengths = get_matches(filt_df, at_ind)

                    if len(matches) == 0:       #No matches found expand search
                        continue
                    elif len(matches) == 1:     #Unique match found
                        pers_id[i] = pers_id[matches[0]]
                        break
                    else:                       #Multiple matches found
                        max_strength = max(strengths)
                        top = [m for m,s in zip(matches, strengths) if s == max_strength]
                        assert(top)
                        if len(top) == 1:
                            pers_id[i] = pers_id[top[0]]
                            break
                        else:
                            salaries = list(df.iloc[top]['StrippedSalary'])
                            sal = df.iloc[i]['StrippedSalary']
                            closest_salary = sorted([(abs(sal - s), t) for s, t in zip(salaries, top)])[-1][1]
                            pers_id[i] = pers_id[closest_salary]
                            break
                    
                else: 
                    pers_id[i] = int(x)
                    x += 1

                
                total_row += 1
                if total_row % 1000 == 0:
                    print('%i: %i: %i: %f' % (y, total_row, x, time.time()- start_time))
                #if total_row % 10000 == 0:
                    #df_out['PrelimId'] = pers_id
                    #tag = '_ally' if all_years else ''
                    #df_out.to_pickle('progress/df_pid' + str(total_row) + tag + '.pkl')


    df_out['PrelimID'] = pers_id
    df_out.to_pickle(sys.argv[2])

if __name__ == "__main__":
    main()

