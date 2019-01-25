#!/usr/bin/env python3
"""
Apply transformations to text columns of dataframe to make them easier to 
combine into clean categories.
"""
import pandas as pd
import time
import string
import re
import pdb
import sys

from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords
stop = stopwords.words('english')


def main():
    col = sys.argv[1]
    out_col = sys.argv[2]

    df = pd.read_pickle(sys.argv[3])

    preprocd = []
    start_time = time.time()
    uniq = list(set(df[col]))
    i = 0
    for r in uniq:
        if type(r)  is not str:
            r = 'No ' + col

        s = r.lower()
        s = s.split('/')[0]     #remove french
        s = s.replace('-',' ')  
        
        if col == 'Employer':    #Remove certain abbreviations noticed in employers
            s = re.sub(r"\b.\'", '', s)
            s = re.sub(r"\be\b", 'board of education', s) 
            s = re.sub(r"\brcssb\b", 'roman catholic separate school boards', s) 
            s = re.sub(r"\bont\b", 'ontario', s)
            s = re.sub(r"\bbrd\b", 'board', s)
            s = re.sub(r"\bctr\b", 'centre', s)
            s = re.sub(r"\bhlth\b", 'health', s)
            s = re.sub(r"\bgen\b", 'general', s)
            s = re.sub(r"\brehab \b", 'rehabilitation', s)
            s = re.sub(r"\bhu\b", 'health unit', s)
            s = re.sub(r"\bdhu\b", 'district health unit', s)
            s = re.sub(r"\bhosp\b", ' hospital', s)

        s = re.sub(r"\b.\'", '', s)

        s = ''.join(c for c in s if c in set(string.ascii_lowercase + ' ')) #Remove punctuation

        s = str(TextBlob(s).correct())

        wl = s.split()
        wl = [Word(w).lemmatize() for w in wl if w not in stop]
        
        i += 1
        if i % 1000 == 0:
            print(time.time() - start_time)
        
        preprocd.append(wl)
       
    stripped = []
    for i, e in df[col].items():
        try:
            ind = uniq.index(e)
            stripped.append(tuple(preprocd[ind]))
        except:
            pass
        if int(i) % 100000 == 0:
            print(time.time() - start_time)


    print(len(stripped))

    df[out_col] = stripped
    df.to_pickle(sys.argv[4])



             


if __name__ == "__main__":
    main()
