#!/usr/bin/env python3
"""
Derive demographic info from name.
"""
import sys
import pandas as pd
from ethnicolr import pred_wiki_name

from distances import *

def main(): 
    df = pd.read_pickle(sys.argv[1])

    df = pred_wiki_name(df, lname_col='Last Name', fname_col='First Name')

    df.to_pickle(sys.argv[2])

if __name__ == "__main__":
    main()
