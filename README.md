# sunshine-list-analysis

I analysed Ontario Public Sector Salary disclosures (aka "The Sunshine List").
The end result is a pandas dataframe that contains a record for each employee
included in any of the disclosures from 1996 to 2017 and their salary for every
year they were included. My main contribution is that employees are tracked
over multiple years; this is non-trivial because the orginal data contains no
unique identifiers so identities must be inferred from names, job titles and
employers. Also included is the code to train a neural network to predict
people's future salaries from past salaries and demographic information.
