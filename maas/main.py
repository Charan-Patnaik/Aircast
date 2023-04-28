# %%
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, Dropout,LSTM
import pickle
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime
import os
from dotenv import load_dotenv
import boto3
import boto3.s3
import botocore

from fastapi import FastAPI
from fastapi.responses import JSONResponse


from s3_model import S3ModelObj
import json


app =  FastAPI()

# %%
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)

s3 = session.resource('s3')

src_bucket = s3.Bucket('damg-aircast')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = '3306'
DB_NAME = os.environ.get('DB_NAME')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# %%
def get_predication_for_aquid(aqsid):
    try:
    # Read data from the SQL table into a dataframe
        print('>>>>>>>>>>>>>>>>  data extraction started')
        inp_data = pd.read_sql_query('SELECT * from aircast.StationsDataDaily WHERE aquid = "%s"' % aqsid, engine)
        print('>>>>>>>>>>>>>>>>  data extraction done')
        ####

        ##################    FEATURE ENGINEERING  #############################

        ####
        # Renaming columns :
        inp_data = inp_data.rename(columns={'collection_timestamp':'datetime','ozone':'OZONE', 'so2':'SO2', 'no2':'NO2','co':'CO','pm2_5':'PM2.5','pm10':'PM10'})
        df = inp_data.copy()
        # Create a boolean array of the same shape as the dataframe
        df = df.replace('NULL',0)
        # Dropping a list of columns with all values 'NULL'
        df = df.drop(columns=df.columns[df.isnull().all()].tolist())
        ## Storing aqs_id:
        aqsid = df['aquid'].iloc[0]
        # Dropping un-required columns
        df = df.drop(columns = ['aquid','id'])

        ## setting 'datetime' column as index
        check = df.copy()
        check = check.set_index('datetime')

        ## Sorting values
        df_sorted = check.sort_values(by='datetime')
        ## Converting type of the Columns data of Pollutants:
        for i in df_sorted.columns:
            df_sorted[i] = df_sorted[i].astype(float)

        df_sorted = df_sorted.tail(48)
        # split a multivariate sequence into samples
        def split_sequences(sequences, n_steps):
            X, y = list(), list()
            for i in range(len(sequences)):
                # find the end of this pattern
                end_ix = i + n_steps
                # check if we are beyond the dataset
                if end_ix > len(sequences)-1:
                    break
                # gather input and output parts of the pattern
                seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
                X.append(seq_x)
                y.append(seq_y)
            return np.array(X), np.array(y)
        ## Pickle generation:
        df = df_sorted.copy()
        values = df.values
        column_names = df.columns.tolist()
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(values)
        n_steps = 24
        X, y = split_sequences(scaled_data, n_steps)
        print(X.size)
        n_features = X.shape[2]

        # demonstrate prediction
        x_input = X 
        x_input = x_input.reshape((24, n_steps, n_features))




        print('>>>>>>>>>>>>>>>>  Feature engineering done')


        # load the model from s3

        print('>>>>>>>>>>>>>>>>  Prediction started')
        filename = '%s.pkl' % aqsid
        
        S3ModelObj.download_model_in_directory(model_pickle_name=filename)


        model = pickle.load(open(f"models/{filename}", 'rb'))

        yhat = model.predict(x_input, verbose=0)
        req = scaler.inverse_transform(yhat)
        date_time_index = pd.date_range(start='00:00:00', end='23:00:00', freq='1H')
        final = pd.DataFrame(index=date_time_index, columns=column_names, data = req)

        final = final.reset_index()
        df.rename(columns={'index':'datetime'}, inplace=True)

        json_records = final.to_json(orient ='records')
        # json_string = json.dumps(df.to_dict(), ensure_ascii=False, orient = 'records')
        
        # parse the JSON data

        return json.loads(json_records)
    except Exception as e:
        print("exception thrown")
        print(e.with_traceback)        


# get_predication_for_aquid(['250250042'])


@app.get('/')
async def index():
    return 'Success! APIs are working for prediction!'


@app.post('/get-prediction-for-station-id/{stations_id}')
async def run_prediction(stations_id):
    try:
        json_result = get_predication_for_aquid(stations_id)
        return JSONResponse(
                status_code= 200,
                content={
                    'success': True, 
                    "predictions": json_result,
                }
            )
    except:
        return JSONResponse(
                status_code= 400,
                content={
                    'success': False, 
                    "message": "not able to predict",
                }
            )
