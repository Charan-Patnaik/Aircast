#%%
import airflow
from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import os
import urllib.request
from datetime import datetime

#%%
# my_arima = ARIMA()

import sys
sys.path.append('/opt/airflow/model/')

#%%
def arima_execution():
    #%%
    df = pd.read_csv('/Users/varshahindupur/Desktop/GitHub/Aircast/data/AirQualityData.csv', sep=',')
    df.head(5)

    #%%
    df.isnull().sum()

    #%%
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['hour'], format='%m/%d/%y %H:%M')
    df.drop(['date', 'hour'], axis=1, inplace=True)
    df.head(5)

    #%%
    last_date = df['datetime'].iloc[-1]
    print(last_date)
    last_date = last_date + timedelta(days=1)
    print(last_date)

    #%%
    # Define the number of days to forecast
    # forecast_horizon = 7
    forecast_horizon = 24

    #%%
    # Split data into training and testing sets
    train, test = train_test_split(df, test_size=forecast_horizon, shuffle=False)

    #%%
    # Generate the date range for the forecast
    forecast_dates = [last_date + timedelta(hours=i) for i in range(1, forecast_horizon+1)]
    print(forecast_dates)

    #%%
    # Fit ARIMA model
    model = ARIMA(df['value'], order=(1, 0, 0))

    #%%
    # Split data into training and testing sets
    results = model.fit()

    #%%
    # Make predictions on test set
    print(test.index[0], test.index[-1])
    predictions = results.predict(start=test.index[0], end=test.index[-1])

    #%%
    # Evaluate model performance on test set
    mse = ((predictions - test['value']) ** 2).mean()
    print('MSE:', mse)

    #%%
    # Forecast future values
    forecast_values = results.forecast(steps=forecast_horizon)

    #%%
    # Combine the forecasted values with the corresponding dates
    forecast = pd.DataFrame({
        'datetime': forecast_dates,
        'value': forecast_values
    })

    #%%
    # Set the date as the index
    forecast = forecast.set_index('datetime')

    #%%
    print(forecast['datetime'], forecast['value'])

    #%%
    return forecast

#%%
import os
import urllib.request
import pandas as pd
from datetime import datetime, timedelta

def read_csv_file(filename):
    df = pd.read_csv(filename, sep='|')
    return df

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
    filename = 'AirQualityData.csv'
    df = read_csv_file(filename)
    
    if given_date_str in '20230422':
        return True
    return False

#%%
def data_extraction_daily():
    today = datetime.today() # get the current date and time as a datetime object
    one_day_ago = today - timedelta(days=1) # subtract one day from the current date
    formatted_date = one_day_ago.strftime('%Y%m%d') # format the date as a string in the desired format
    
    if not datetime_if_exists(formatted_date):
        combine_data(filename, csv_file)
    else:
        filename = extract_data(formatted_date)


# %%
dag = DAG(
    dag_id = "modelservice",
    schedule = None,   # https://crontab.guru/
    start_date = days_ago(0),
    catchup = False,
    dagrun_timeout = timedelta(minutes=60),
    tags = ["damg7245"]
)

with dag:

    air_data_extraction_daily = PythonOperator(
        task_id='air_data_extraction_daily',
        python_callable= data_extraction_daily,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )

    arima_data_modeling = PythonOperator(
        task_id='arima_data_modeling',
        python_callable= arima_execution,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )

    # Flow
    air_data_extraction_daily >> arima_data_modeling

