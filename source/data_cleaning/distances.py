import difflib as dl

n_sect = 12
n_years = 22
start_year = 1996
years = range(n_years)

CY = 'Calendar Year'
FN = 'StrippedFirstName'
LN = 'StrippedLastName'
MI = 'StrippedMiddleInitial'
FI = 'StrippedFirstInitial'
TL = 'StrippedTitle'
N = 'StrippedName'
S = 'StrippedSalary'

def seqm(a, b):
    #Compute Radcliffe-Oberhelp Gestalt pattern match distance
    return dl.SequenceMatcher(None,' '.join(a),' '.join(b)).ratio()

def jaccard(l1, l2):
    #Compute Jaccard distance
    if not l2 or not l1:
        return 0

    intersection = len(list(set(l1).intersection(l2)))
    union = (len(l1) + len(l2)) - intersection
    return float(intersection / union)

def my_jaccard(l1, l2, freq_words):
    #Compute Jaccard distance, but exclude common words
    intersection = len(list(set(l1).intersection(l2)))
    l1_p = [i for i in l1 if i not in freq_words]
    l2_p = [i for i in l2 if i not in freq_words]

    if not l2_p or not l1_p:
        return 0
    
    intersectionp = len(list(set(l1_p).intersection(l2_p)))
    union = (len(l1) + len(l2)) - intersectionp

    return max(float(intersection / union), 1.0)


