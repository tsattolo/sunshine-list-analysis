# sunshine-list-analysis

I analysed Ontario Public Sector Salary disclosures (aka "The Sunshine List").
The end result is a pandas dataframe that contains a record for each employee
included in any of the disclosures and their salary for every
year they were included. My main contribution is that employees are tracked
over multiple years; this is non-trivial because the orginal data contains no
unique identifiers so identities must be inferred from names, job titles and
employers. Also included is the code to train a neural network to predict
people's future salaries from past salaries and demographic information.

## Usage:
# Data Cleaning
Download raw csv files from https://www.ontario.ca/page/public-sector-salary-disclosure.

Run clean.sh and give it a glob that matches all the dowloaded csvs (and nothing else). Ex:
```
clean.sh "Datasets/*.csv"
```
This will run for a long time (about 4 days). I've included the final
result in this repository for those who would prefer not to wait.

# Neural Net

Run nn.py and give it the dataframe generated above. Ex:
```
nn.py 'df_final.pkl'
```
This performs some preprocessing and caches the result. 
Various parameters, both in nn.py and nn_settings.py, can
be used to tweak the neural network.
