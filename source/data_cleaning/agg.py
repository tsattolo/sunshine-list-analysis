#!/usr/bin/env python3
"""
Aggregate differently spelled entries in a column that represent the same entity
"""

import csv
import numpy as np
import json
import pandas as pd
import pdb
from collections import Counter
import sys
import os

from distances import *

frst_thresh = 0.95
scnd_thresh = 0.75
scnd_gap = 0.9
freq_thresh = 0.02 

def find_sames_uniq(old, new, y, freq_words):
    dist_fns = [(jaccard, []),(seqm, []), (my_jaccard, freq_words), (jaccard, [])] 
    for l in new.values(): 
        for mydist, ctx in dist_fns:
            matches = []
            for k, v in old.items(): 
                for s in v: 
                    if ctx:
                        matches.append((mydist(l,s[1], ctx), k))
                    else:
                        matches.append((mydist(l,s[1]), k))
            
            break_outer = False
            matches = sorted(matches, reverse=True)
            while matches:
                frst = matches[0]
                if len(matches) >= 2:
                    scnd = matches[1] 
                else: scnd = (1,1)

                if frst[0] > frst_thresh or (frst[0] > scnd_thresh and float(scnd[0]) < (scnd_gap * frst[0])):
                    if old[frst[1]][-1][0][0] == y:
                        if old[frst[1]][-1][0][1] >  frst[0]:       #if we've found a match that's good enough but the string that's been added already is a better match
                            pass
                        else:
                            #Swap string at unique ID for this year
                            temp = old[frst[1]][-1][1]
                            old[frst[1]][-1] = ((y,frst[0]),l)
                            l = temp
                            break
                    else:
                        break_outer = True
                        old[frst[1]].append(((y, frst[0]),l))
                        break

                del(matches[0])

            if break_outer:
                break


        else:
            old[len(old)] = [((y,1), l)]
    return

def find_sames_not_uniq(old, new, y, freq_words):
    dist_fns = [(jaccard, []),(seqm, []), (my_jaccard, freq_words)] 
    for l in new.values(): 
        for mydist, ctx in dist_fns:
            matches = []
            for k, v in old.items():
                for s in v: 
                    if ctx:
                        matches.append((mydist(l,s[1], ctx), k))
                    else:
                        matches.append((mydist(l,s[1]), k))
            
            if not matches:
                continue    #Need to execute else

            frst = max(matches)
            if frst[0] > frst_thresh:
                old[frst[1]].append((y,l))
                break

            if len(matches) == 1:
                continue
                
            scnd =  np.partition(matches, -2)[-2]
            if frst[0] > scnd_thresh and float(scnd[0]) < (scnd_gap * frst[0]):
                old[frst[1]].append((y,l))
                break

        else:
            old[len(old)] = [(y, l)]
    return

def get_uniq_dicts(fr, col, rep=[]):
    a = [list(x) for x in set(tuple(x) for x in fr[col])]
    return dict(zip(range(len(a)),a))


def create_col_dict_uniq(frl, col, filt, freq_words, folder):
    #Create a dictionnary that gather all the variant spelling of a column
    #(employer or job title) assuming that different spellings in the same
    # year always represent real differences.
    col_uniq = [get_uniq_dicts(fr.loc[fr[filt[0]] == filt[1]], col) for fr in frl]
    col_dict = dict([(a,[((0,1.0),b)]) for a,b in col_uniq[0].items()])
    for y in range(1, len(col_uniq)):
        find_sames_uniq(col_dict, col_uniq[y], y, freq_words)

    with open(folder + str(filt[1]) + col + 'Dict.json', 'w') as f:
        f.write(json.dumps(col_dict))    

def create_col_dict_not_uniq(frl, col, filt, freq_words, folder):
    #Create a dictionnary that gather all the variant spelling of a column
    #(employer or job title). Different spelling in the same year can
    # be grouped.

    col_uniq = [get_uniq_dicts(fr.loc[fr[filt[0]] == filt[1]], col) for fr in frl]
    col_dict = dict()
    for y in range(0, len(col_uniq)):
        find_sames_not_uniq(col_dict, col_uniq[y], y, freq_words)

    with open(folder + str(filt[1]) + col + 'Dict.json', 'w') as f:
        f.write(json.dumps(col_dict))    

def get_freq_words(thresh, df):
    flat_list = [item for sublist in set(df) for item in sublist]
    cn = Counter(flat_list)
    return [a for a,b in cn.most_common() if b > thresh*len(flat_list)]

def main():
    folder = sys.argv[1]

    try: os.mkdir(folder)
    except FileExistsError: pass

    col = sys.argv[2]
    pickle = sys.argv[3]
    unique_in_year = len(sys.argv) >= 5 and sys.argv[4] == '--unique'
    with open('SectorDict.json', 'r') as sd:
        sector_dict = json.loads(sd.read())

    df = pd.read_pickle(pickle)
    
    frl = [df.loc[df['Calendar Year'] == start_year + y] for y in years] 
    seconded_sectors = [k for k,v in sector_dict.items() if 'seconded' in v[0]]
    for k in sector_dict.keys():
        if k in seconded_sectors: continue
        k = int(k)
        freq_words = get_freq_words(freq_thresh, df[col].loc[df['SectorID'] == k])
        if unique_in_year:  
            create_col_dict_uniq(frl, col, ('SectorID', k), freq_words, folder)
        else:
            create_col_dict_not_uniq(frl, col, ('SectorID',k), freq_words, folder)
                
             
if __name__ == "__main__":
    main()
