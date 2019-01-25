#!/usr/bin/env python3
"""
Derive demographic info from name.
"""
import sys
import pandas as pd
import time
from chicksexer import predict_genders

from distances import *

def main(): 
    df = pd.read_pickle(sys.argv[1])
    
    prob_female = []
    gender = []

    start_time = time.time()

    names = [' '.join(e) for e in df['StrippedName']]
    gender_pred = []

    for i in range(0,len(names), 10000):
        gender_pred.extend(predict_genders(names[i: i + 10000]))
        print('%i: %f' % (i, time.time() - start_time))

        
    prob_female = [e['female'] for e in gender_pred]
    gender = ['F' if p >= 0.5 else 'M' for p in prob_female]

    df['Gender'] = gender
    df['Probability Female'] = prob_female

    df.to_pickle(sys.argv[2])

if __name__ == "__main__":
    main()
