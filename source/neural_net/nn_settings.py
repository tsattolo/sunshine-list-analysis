import os

n_sct = 12   #Number of sectors to include in analysis
n_emp = 100  #Number of employers to include in analysis
n_jbt = 100  #Number of job titles to include in analysis

years = range(1996,2018)
n_years = 22

ts_thresh = 4 #Minumum number of years a person has to be found in the dataset to be included in analysis
n_target = 1  #Number of years in the future to predict
assert(ts_thresh >= n_target)

n_onehot = n_sct + n_emp + n_jbt + n_years - ts_thresh

inflation = 0.02

sal_cols = ['Salary' + str(y) for y in years]
ben_cols = ['Benefits' + str(y) for y in years]

other_cols = ['Probability Female', 'Asian,GreaterEastAsian,EastAsian',
              'Asian,GreaterEastAsian,Japanese', 'Asian,IndianSubContinent',
              'GreaterAfrican,Africans', 'GreaterAfrican,Muslim',
              'GreaterEuropean,British', 'GreaterEuropean,EastEuropean',
              'GreaterEuropean,Jewish', 'GreaterEuropean,WestEuropean,French',
              'GreaterEuropean,WestEuropean,Germanic', 'GreaterEuropean,WestEuropean,Hispanic',
              'GreaterEuropean,WestEuropean,Italian', 'GreaterEuropean,WestEuropean,Nordic']


n_input = n_onehot + (n_years - n_target) + len(other_cols) 

settings_list = [n_sct, n_emp, n_jbt, n_years, ts_thresh, n_target]
settings_string = '_'.join([str(n) for n in settings_list])

data_folder = 'dataset/'
model_folder = 'saved_models/'

try: os.mkdir(data_folder)
except FileExistsError: pass

try: os.mkdir(model_folder)
except FileExistsError: pass
