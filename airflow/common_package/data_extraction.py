#%%
import pandas as pd
from datetime import datetime, timedelta
import os
import urllib.request
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime, text

load_dotenv()


DB_USER = os.environ.get('SQL_DB_USER')
DB_PASSWORD = os.environ.get('SQL_DB_PASSWORD')
DB_HOST = os.environ.get('SQL_DB_HOST')
DB_PORT = '3306'
DB_NAME = os.environ.get('SQL_DB_NAME')


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

directory_with_raw_files = 'data/raw'


#%%
def _get_zero_appended(value: int) -> str:
    if value < 10:
        return f'0{value}'
    else:
        return str(value)
    

def _download_file(url, directory, filename):
    urllib.request.urlretrieve(url, os.path.join(directory, filename))


def _initialize_directory():
    if not os.path.exists('data'):
        os.makedirs('data')
        os.makedirs(directory_with_raw_files)
        print('data directory created successfully')

    
    files = os.listdir(directory_with_raw_files)

    # Loop through the files and remove each one
    for file_name in files:
        file_path = os.path.join(directory_with_raw_files, file_name)
        os.remove(file_path)


def _download_files_for_day(date: str):
    files_downloaded = []

    year = date[:4]
    
    for i in range(24):
        url = f'https://s3-us-west-1.amazonaws.com/files.airnowtech.org/airnow/{year}/{date}/HourlyData_{date}{_get_zero_appended(i)}.dat'
        directory = './data/raw'
        filename = f'HourlyData_{date}{_get_zero_appended(i)}.dat'
        
        files_downloaded.append(f"{directory}/{filename}")
        
        _download_file(url, directory, filename)




def _build_combine_dataframe():
    # List of CSV files in the directory
    csv_files = [os.path.join(directory_with_raw_files, file) for file in os.listdir(directory_with_raw_files) if file.endswith('.dat')]
    
    column_names = ['date', 'hour', 'AQSID', 'sitename', 'GMT offset', 'parameter name', 'reporting units', 'value', 'datasource']


    dfs = [pd.read_csv(file, sep='|', names=column_names) for file in csv_files]

    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    print("combine dataframe", combined_df.shape)

    stations_only_with_param = pd.read_csv('https://damg-aircast.s3.amazonaws.com/miscellaneous/station_with_params.csv')
    stations_only_with_param.drop(['Unnamed: 0.1', 'Unnamed: 0', 'Latitude', 'Longitude', 'CountyName', 'parameter name', 'SiteName'], axis=1, inplace=True)

    print("stations only: ", stations_only_with_param.shape)

    merged_df = pd.merge(combined_df, stations_only_with_param, on='AQSID', how='right')
    merged_df['datetime'] = pd.to_datetime(merged_df['date'] + ' ' + merged_df['hour'], format='%m/%d/%y %H:%M')
    merged_df.drop(['date', 'hour'], axis=1, inplace=True )

    values_to_keep = ['OZONE', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2']
    merged_df_with_specific_val = merged_df.loc[merged_df['parameter name'].isin(values_to_keep)]

    df_pivot = merged_df_with_specific_val.pivot(index=['datetime', 'AQSID', 'sitename', 'GMT offset', 'datasource'], 
                    columns='parameter name', 
                    values='value').reset_index()
    
    df_pivot = df_pivot.rename(columns={'OZONE': 'OZONE (PPB)', 'PM2.5': 'PM2.5 (UG/M3)', 'CO': 'CO (PPM)'})
    pivot_df = df_pivot.sort_values(by='datetime', ascending=False)
    print("shape of engineered data: ", pivot_df.shape)


    new_table_with_column = df_pivot.rename(columns={'datetime':'collection_timestamp', 'AQSID':'aquid', 'OZONE (PPB)':'ozone', 'PM2.5 (UG/M3)':'pm2_5', 'CO (PPM)':'co', 'SO2':'so2', 'NO2':'no2', 'PM10':'pm10'})
    new_table_with_column.drop(['sitename', 'GMT offset', 'datasource'], axis=1, inplace=True)


    new_table_with_column = new_table_with_column.where(pd.notnull(new_table_with_column), 'NULL')
    # new_table_with_column

    new_table_with_column['collection_timestamp'] = new_table_with_column['collection_timestamp'].dt.strftime('%Y-%m-%dT%H:%M')


    json_list = new_table_with_column.to_dict(orient='records')
    print("cobine json data")
    return json_list


def _insert_json_in_table(json_data):
    # Define database connection details
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


    metadata = MetaData()
    metadata.bind = engine
    # Name of the table to insert data into
    
    my_table = Table('StationsData', metadata,
                 Column('id', Integer, primary_key=True, index=True, autoincrement=True),
                 Column('collection_timestamp', DateTime),
                Column('aquid', String(255), unique=False),
                Column('ozone', String),
                Column('so2', String),
                Column('no2', String),
                Column('co', String),
                Column('pm2_5', String),
                Column('pm10', String),
                 )
    
        
    my_table_daily = Table('StationsDataDaily', metadata,
                 Column('id', Integer, primary_key=True, index=True, autoincrement=True),
                 Column('collection_timestamp', DateTime),
                Column('aquid', String(255), unique=False),
                Column('ozone', String),
                Column('so2', String),
                Column('no2', String),
                Column('co', String),
                Column('pm2_5', String),
                Column('pm10', String),
                 )
    
    conn = engine.connect()

    # execute the SQL query to truncate a table
    truncate_query = text("TRUNCATE TABLE StationsDataDaily")
    conn.execution_options(autocommit=True).execute(truncate_query)
    print("data truncated in SQL Successfully")


    conn.execution_options(autocommit=True).execute(my_table.insert(), json_data)
    print("all data inserted in SQL Successfully")
    

    conn.execute(my_table_daily.insert(), json_data)
    print("daily data inserted in SQL Successfully")

    conn.close()

def _insert_two_days_json_in_table(json_data):
    # Define database connection details
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


    metadata = MetaData()
    metadata.bind = engine
    # Name of the table to insert data into
        
    my_table_daily = Table('StationsDataDaily', metadata,
                 Column('id', Integer, primary_key=True, index=True, autoincrement=True),
                 Column('collection_timestamp', DateTime),
                Column('aquid', String(255), unique=False),
                Column('ozone', String),
                Column('so2', String),
                Column('no2', String),
                Column('co', String),
                Column('pm2_5', String),
                Column('pm10', String),
                 )
    
    conn = engine.connect()

    # execute the SQL query to truncate a table
    truncate_query = text("TRUNCATE TABLE StationsDataDaily")
    conn.execution_options(autocommit=True).execute(truncate_query)
    print("data truncated in SQL Successfully")
    

    conn.execute(my_table_daily.insert(), json_data)
    print("daily data inserted in SQL Successfully")

    conn.close()


#%%
def data_extraction_daily():
    today = datetime.today() # get the current date and time as a datetime object
    one_day_ago = today - timedelta(days=1) # subtract one day from the current date
    formatted_date = one_day_ago.strftime('%Y%m%d')
    
    print(formatted_date)

    _initialize_directory()
    _download_files_for_day(formatted_date)
    result_json = _build_combine_dataframe()
    _insert_json_in_table(result_json)


def data_extraction_two_days():
    today = datetime.today() # get the current date and time as a datetime object
    one_day_ago = today - timedelta(days=1) # subtract one day from the current date
    two_day_ago = today - timedelta(days=2) # subtract one day from the current date
    three_day_ago = today - timedelta(days=3) # subtract one day from the current date
    formatted_date = one_day_ago.strftime('%Y%m%d')
    formatted_two_date = two_day_ago.strftime('%Y%m%d')
    formatted_three_date = three_day_ago.strftime('%Y%m%d')
    
    print(formatted_date)

    _initialize_directory()
    _download_files_for_day(formatted_date)
    _download_files_for_day(formatted_two_date)
    _download_files_for_day(formatted_three_date)
    result_json = _build_combine_dataframe()
    _insert_two_days_json_in_table(result_json)


def clear_cache():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


    conn = engine.connect()
    
    truncate_query = text("TRUNCATE TABLE ZipDataDailyCache")
    conn.execution_options(autocommit=True).execute(truncate_query)
    print("Data truncated in SQL Successfully")