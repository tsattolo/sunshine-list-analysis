#!/usr/bin/env python3
"""
Create pandas dataframe from downloaded csv files and categorize sectors
"""

import csv
import pandas as pd
import sys
import json
import pdb

def main():
    frl = []
    for i in range(2, len(sys.argv)-1):
        df = pd.read_csv(sys.argv[i],  encoding = "ISO-8859-1")
        frl.append(df)


    #Create SectorID columns to categorize sectors as integers (categorization was done manually)
    with open('SectorDict.json', 'r') as sd:
        sector_dict = json.loads(sd.read())
    for df in frl:
        for i in range(len(df)):
            for k, v in sector_dict.items():
                if df.at[i, 'Sector'].lower() in v:
                    df.at[i, 'SectorID'] = int(k)

    df = pd.concat(frl, sort=False).reset_index()

    #Fix for job titles that contain commas
    latest_year = 1996
    for i, r in df.iterrows():
        try:
            y = int(r['Calendar Year'])
            latest_year = y
            df.at[i,'Calendar Year'] = latest_year        
        except ValueError:
            df.at[i, 'Job Title'] = df.at[i, 'Job Title'] + df.at[i,'Calendar Year']  
            df.at[i,'Calendar Year'] = latest_year

    del df['Unnamed: 8']
    df.to_pickle(sys.argv[1])

if __name__ == "__main__":
    main()
