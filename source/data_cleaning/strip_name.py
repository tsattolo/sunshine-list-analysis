#!/usr/bin/env python3
"""
Split names into logical parts: First Names, First Initials, Middle Initials and Last Names
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
    fns = df['First Name']
    lns = df['Last Name']

    i = 0
    start_time = time.time()

    titles = ['hon', 'dr']
    fn_col = []
    ln_col = []
    mi_col = []
    fi_col = []
    ttl_col = []
    n_col = []

    for f, l in zip(fns, lns):
        if type(f) is not str:
            f = 'NoName'
        if type(l) is not str:
            l = 'NoName'
        
        f = f.lower()
        l = l.lower()
        f = ''.join(c for c in f if c in set(string.ascii_lowercase + ' '))
        l = ''.join(c for c in l if c in set(string.ascii_lowercase + ' '))

        f = f.split()
        l = l.split()

        ttl = []
        for t in titles:
            if t in f:
                ttl.append(t)

        fi = []
        fn = []
        mi = []

        for w in f:
            if len(w) == 1:
                if fn:
                    mi.append(w)
                else:
                    fi.append(w)
            else:
                fn.append(w)

        fn_col.append(fn)        
        fi_col.append(fi)        
        mi_col.append(mi)        
        ln_col.append(l)
        ttl_col.append(ttl)
        n_col.append(ttl + fi +fn + mi + l)

        assert(len(ttl_col) == len(ln_col))
        
    df['StrippedFirstName'] = fn_col
    df['StrippedLastName'] = ln_col
    df['StrippedMiddleInitial'] = mi_col
    df['StrippedFirstInitial'] = fi_col
    df['StrippedTitle'] = ttl_col
    df['StrippedName'] = n_col 

    outfile = sys.argv[2]
    df.to_pickle(outfile)

if __name__ == "__main__":
    main()
