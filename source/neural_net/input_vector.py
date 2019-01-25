#!/usr/bin/env python3
"""
Convert dataframe into matrices for simple consumption by neural network.
Also split data into training, validation and test sets.
"""
import sys
import pandas as pd
import pdb
import time
import collections as coll
import numpy as np

from nn_settings import *


def normalize(array):
    for col in array:
        m = np.mean(col)
        col -= m
        std = np.std(col)
        print(m, std)
        if std != 0:
            col /= std

def check_ts(ts):
    all_zero = True
    last_zero = True
    for t in ts:
        if t != 0 and last_zero and not all_zero:
            print('Problem')
        if t > 0 and all_zero:
            allzero = False
        last_zero = t == 0

def get_ts(r):

    ia = [(1 + inflation) ** i for i in range(n_years)]
    ts = [(r[a] + r[b]) / c for a, b, c in zip(sal_cols, ben_cols, ia)]
    
    #check_ts(ts)

    sts = [t for t in ts if t != 0]
    return sts, ts.index(sts[0])
    
def get_freq_mapping(df, col, n):
    cnt = coll.Counter(df[col])
    return {a[0]: b  for a, b in zip(cnt.most_common(n), range(n))}

def main(): 
    df = pd.read_pickle(sys.argv[1])
    
    sct_dict = get_freq_mapping(df, 'SectorID', n_sct)
    jbt_dict = get_freq_mapping(df, 'StrippedJobID', n_jbt)
    emp_dict = get_freq_mapping(df, 'StrippedEmpID', n_emp)

    dataset = np.zeros((len(df), n_onehot + (n_years - n_target) + len(other_cols) + n_target))

    n = 0
    for i, r in df.iterrows():
        if i % 10000 == 0:
            print(i)

        ts, y= get_ts(r)
        if len(ts) <= ts_thresh:
            continue
    
        target_arr = np.array(ts[-n_target:])
        ts_arr = np.concatenate((ts[0]*np.ones(n_years - len(ts)), ts[:-n_target]))

        y_arr = np.zeros(n_years - ts_thresh)
        y_arr[y] = 1.0

        sct_arr = np.zeros(n_sct)
        jbt_arr = np.zeros(n_jbt)
        emp_arr = np.zeros(n_emp)

        try:
            sct_arr[sct_dict[r['SectorID']]] = 1.0
            jbt_arr[jbt_dict[r['StrippedJobID']]] = 1.0
            emp_arr[emp_dict[r['StrippedEmpID']]] = 1.0
        except (ValueError, KeyError):
            pass

        other_arr = np.array(list(r[other_cols]))

        dataset[n] = np.concatenate((sct_arr, emp_arr, jbt_arr, y_arr, ts_arr, other_arr, target_arr))
        n += 1

    dataset = dataset[:n]
    np.random.shuffle(dataset)

    split1 = int(0.8*n)
    split2 = int(0.9*n)

    train = dataset[:split1]
    valid = dataset[split1:split2]
    test = dataset[split2:]

    #Normalize by column, but exclude one-hot features
    normalize(train.T)
    normalize(valid.T)
    normalize(test.T)

    np.save(data_folder + 'train_' + settings_string, train)
    np.save(data_folder + 'valid_' + settings_string, valid)
    np.save(data_folder + 'test_' + settings_string, test)
    


if __name__ == "__main__":
    main()
