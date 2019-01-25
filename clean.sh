#!/bin/bash

#Build dataframe from csvs
mkdir interim_data
./source/data_cleaning/build_dataframe.py 'interim_data/df_built.pkl' $1

./source/data_cleaning/strip_column.py 'Employer'  'StrippedEmp' 'interim_data/df_built.pkl' 'interim_data/df_stripped_emp.pkl' 
./source/data_cleaning/agg.py 'interim_data/Employer/' 'StrippedEmp' 'interim_data/df_stripped_emp.pkl' --unique
./source/data_cleaning/gloves.py 'interim_data/Employer/' 'StrippedEmp'
./source/data_cleaning/add_column_id.py 'interim_data/Employer/gloved/' 'StrippedEmp' 'interim_data/df_stripped_emp.pkl' 'interim_data/df_emp_id.pkl' 

./source/data_cleaning/strip_column.py 'Job Title' 'StrippedJob' 'interim_data/df_emp_id.pkl' 'interim_data/df_stripped_job.pkl' 
./source/data_cleaning/agg.py 'interim_data/Job/' 'StrippedJob' 'interim_data/df_stripped_job.pkl'
./source/data_cleaning/gloves.py 'interim_data/Job/' 'StrippedJob'
./source/data_cleaning/add_column_id.py 'interim_data/Job/gloved/' 'StrippedJob' 'interim_data/df_stripped_job.pkl' 'interim_data/df_column_id.pkl'

./source/data_cleaning/strip_name.py 'interim_data/df_column_id.pkl' 'interim_data/df_stripped_name.pkl'
./source/data_cleaning/strip_salary.py 'interim_data/df_stripped_name.pkl' 'interim_data/df_stripped_salary.pkl'

./source/data_cleaning/people.py 'interim_data/df_stripped_salary.pkl' 'interim_data/df_prelim_id.pkl'
./source/data_cleaning/remove_dupes.py 'interim_data/df_prelim_id.pkl' 'interim_data/df_real_id.pkl' 
./source/data_cleaning/make_ts.py 'interim_data/df_real_id.pkl' 'interim_data/df_timeseries.pkl'

pip3 install chicksexer
./source/data_cleaning/mine_name_gender.py 'interim_data/df_timeseries.pkl' 'interim_data/df_gender.pkl' 
# This is necessary because the packages used to infer ethnicity and gender
# are built on incompatible version on tensorflow
python3 -m venv ethnicolr_env
source ethnicolr_env/bin/activate
pip3 install ethnicolr
./source/data_cleaning/mine_name_ethnicity.py 'interim_data/df_gender.pkl' 'df_final.pkl'
deactivate
