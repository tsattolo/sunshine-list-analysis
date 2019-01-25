#!/usr/bin/env python3
"""
If any of the categories that columns were aggregated into fit together "like a glove"
(i.e. they never both exist in the same year and the years either exist are adjacent)
then aggregate these with a lower threshold then we used before.
"""
import json
import pdb
import sys 
import numpy as np
import difflib as dl
import os
from distances import *

match_thresh = 0.7
min_adj = 5 

def match_strength(a,b):
    return max(seqm(a,b), jaccard(a,b))

def main():
    folder = sys.argv[1] +'/'
    col = sys.argv[2]
    
    outfolder = folder + 'gloved/'
     
    try: os.mkdir(outfolder)
    except Exception: pass

    for d in range(n_sect):
        with open(folder + str(d) + col + 'Dict.json') as f:
            cdict = json.loads(f.read())
        
        gloved  = [1]

        while gloved:
            print(d, end='') 
            new_cdict = []
            gloved  = []

            for k0, v0 in cdict.items():
                if k0 in gloved:
                    continue
                ys = list(set([e[0][0] if type(e[0]) is list else e[0] for e in v0]))
                for k1, v1 in cdict.items():
                    if k1 >= k0 or k1 in gloved:
                        continue
                    ys1 = list(set([e[0][0] if type(e[0]) is list else e[0] for e in v1]))
                    all_ys = sorted(ys + ys1) 
                    if len(all_ys) > min_adj and  all(np.diff(all_ys) == 1):
                        for a in v0:
                            if any([match_strength(a[1],b[1]) >= match_thresh for b in v1]):
                                new_cdict.append(sorted(v0 + v1))
                                gloved.append(k0)
                                gloved.append(k1)
                                break
        
            for k0, v0 in cdict.items():
                if k0 not in gloved:
                    new_cdict.append(v0)

            cdict = dict(zip(range(len(new_cdict)), new_cdict))

        
        
        with open(outfolder + str(d) + col + 'Dict.json', 'w') as f:
            f.write(json.dumps(cdict))    

if __name__ == "__main__":
    main()
