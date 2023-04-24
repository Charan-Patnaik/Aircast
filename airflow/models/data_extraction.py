#%%
from datetime import timedelta
import pandas as pd
from datetime import datetime, timedelta
import os
import urllib.request
from datetime import datetime

#%%
def read_csv_file(filename):
    df = pd.read_csv(filename, sep='|')
    return df

#%%
def get_zero_appended(value: int) -> str:
    if value < 10:
        return f'0{value}'
    else:
        return str(value)

#%%
def extract_data(today):
    directory = './data/'
    for i in range(24):
        year = today[:4]
        if not os.path.exists(directory):
            os.makedirs(directory)
        url = f'https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/{year}/{today}/HourlyData_{today}{get_zero_appended(i)}.dat'
        print(url)
        filename_dat = f'HourlyData_{today}{get_zero_appended(i)}.dat'
        if not os.path.exists(os.path.join(directory, filename_dat)):
            urllib.request.urlretrieve(url, os.path.join(directory, filename_dat))

    return filename_dat

#%%
def combine_data(file_dat, csv_file):
    directory = './data/'
    file = 'AirQualityData.csv'
    column_names = ['date', 'hour', 'AQSID', 'sitename', 'GMT offset', 'parameter name', 'reporting units', 'value', 'datasource']  
    dat_file = pd.read_csv(file_dat, delimiter='|')
    csv_file = pd.read_csv(csv_file, delimiter='|')
    merged_file = pd.merge(dat_file, csv_file, on=column_names)
    merged_file.to_csv(csv_file, index=False)
    
#%%
def datetime_if_exists(given_date_str):
    filename = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData.csv'
    df = read_csv_file(filename)
    
    if given_date_str in '20230423':
        return True
    return False

#%%
def data_extraction_daily():
    today = datetime.today() # get the current date and time as a datetime object
    one_day_ago = today - timedelta(days=1) # subtract one day from the current date
    formatted_date = one_day_ago.strftime('%Y%m%d') # format the date as a string in the desired format
    filename = ''
    csv_file = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData.csv'

    if not datetime_if_exists(formatted_date):
        combine_data(filename, csv_file)
    else:
        filename = extract_data(formatted_date)

#%%
def data_segregation(filename):
    #%%
    # read file
    filename = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData.csv'
    df =  pd.read_csv(filename, sep=',')
    df.head(2)
    #%%
    # Convert date and hour columns to datetime and combine them
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['hour'], format='%m/%d/%y %H:%M')
    df.head(2)
    #%%
    # AQSID, aquid, datetime, ozone, no, no2, co, pm2_5, pm10
    pivot_df = df.pivot_table(index=['AQSID', 'datetime'], columns='parameter name', values='value')
    pivot_df = pivot_df.reset_index()
    # Rename the columns to match the desired output format
    pivot_df.columns = ['aquid', 'collection_timestamp', 'AG', 'AL', 'AS', 'AT', 'CH', 'co', 'CR', 'CU', 'FE', 'HG', 'K', 'MN', 'NA', 'NI', 'no', 'no2', 'ozone', 'P', 'PB', 'pm10', 'pm2_5', 'SB', 'ZN']
    # Sort the columns in the desired order
    pivot_df = pivot_df[['aquid', 'collection_timestamp', 'ozone', 'no', 'no2', 'co', 'pm2_5', 'pm10']]
    pivot_df = pivot_df.sort_values(by='collection_timestamp', ascending=False)
    pivot_df.head(15)
    #%%
    # replace NaN values with NULL
    pivot_df = pivot_df.fillna('NULL')
    print(pivot_df)
    #%%
    pivot_df.to_csv('/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData_Modified.csv', sep=',', index=False)


#%%
data_extraction_daily()
# %%
filename = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData.csv'
data_segregation(filename)