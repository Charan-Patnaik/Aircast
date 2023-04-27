import os
from dotenv import load_dotenv
import boto3
import boto3.s3
import botocore
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime, text
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, LSTM
# import pickle

session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)

s3 = session.resource('s3')

src_bucket = s3.Bucket('damg-aircast')

DB_USER = os.environ.get('SQL_DB_USER')
DB_PASSWORD = os.environ.get('SQL_DB_PASSWORD')
DB_HOST = os.environ.get('SQL_DB_HOST')
DB_PORT = '3306'
DB_NAME = os.environ.get('SQL_DB_NAME')


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


my_list = ['100010002', '100031007', '100031008', '100031010', '100031013', '100032004', '100051002', '100051003', '110010041', '110010043', '110010050', '110010051', '230010014', '230031100', '230052003', '230112001', '230130004', '230172011', '230190017', '230194008', '230310040', '230312002', '240031003', '240051007', '240053001', '240090011', '240130001', '240150003', '240170010', '240190004', '240199991', '240210037', '240251001', '240259001', '240290002', '240313001', '240330030', '240338003', '240339991', '240430009', '250010002', '250036001', '250051004', '250051006', '250092006', '250095005', '250130008', '250130018', '250154002', '250170009', '250230005', '250250002', '250250042', '250250044', '250270015', '250270024', '330012004', '330050007', '330074002', '330090010', '330111011', '330115001', '330131006', '330150014', '330150016', '340010006', '340030006', '340030010', '340070002', '340110007', '340150002', '340170006', '340171002', '340171003', '340190001', '340210005', '340219991', '340230011', '340250005', '340273001', '340290006', '340315001', '340390003', '340390004', '340392003', '340410007', '360010012', '360050080', '360050110', '360050112', '360050133', '360130006', '360270007', '360290002', '360290023', '360291014', '360310003', '360410005', '360450002', '360470052', '360470118', '360550015', '360590005', '360610115', '360610135', '360631006', '360652001', '360671015', '360710002', '360750003', '360790005', '360810120', '360810124', '360810125', '360850111', '360870005', '360910004', '361010003', '361030002', '361030004', '361030009', '361099991', '361173001', '361192004', '420010001', '420110006', '420110011', '420130801', '420150011', '420270100', '420279991', '420290100', '420410101', '420430401', '420431100', '420450109', '420479991', '420550001', '420630004', '420690101', '420692006', '420710012', '420770004', '420810100', '420890002', '420910013', '420950025', '421010004', '421010024', '421010048', '421010055', '421010057', '421010075', '421010076', '421174000', '421330008', '421330011', '440030002', '440070022', '440071010', '440090007', '500030004', '500070007', '500210002', '510130020', '510590030', '511071005', '540030003']



def generate_mode_for_ma():
    counter = 0


    for aqsid in my_list:

        ####

        #####################   DATA EXTRACTION FROM AWS DataBase #############################

        ####
        # Read data from the SQL table into a dataframe
        # 
        print('>>>>>>>>>>>>>>>>  data extraction started')
        
        inp_data = pd.read_sql_query('SELECT * from aircast.StationsData WHERE aquid = "%s"' % aqsid, engine)

        print('>>>>>>>>>>>>>>>>  data extraction done')

        ####

        ##################    FEATURE ENGINEERING  #############################
        print('>>>>>>>>>>>>>>>>  Feature engineering started')
        ####
        # Renaming columns :
        inp_data = inp_data.rename(columns={'collection_timestamp':'datetime','ozone':'OZONE', 'so2':'SO2', 'no2':'NO2','co':'CO','pm2_5':'PM2.5','pm10':'PM10'})
        print(len(inp_data))
        df = inp_data.copy()
        
        if df.empty: 
            print('DataFrame is empty')
            counter = counter + 1
            print(counter)
        else:
            print('DataFrame is not empty')
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
            print(df_sorted.info(),'df_sorted_info()')

            print('>>>>>>>>>>>>>>>>  Feature engineering done')

            ####

            ##################    MODELING AND PICKLE GENERATION  #############################

            ####

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

            print('>>>>>>>>>>>>>>>> pickle generation started for :', aqsid)
            ## Pickle generation:
            df = df_sorted.copy()
            print(df.info(),'df_info()')
            values = df.values
            column_names = df.columns.tolist()
            scaler = MinMaxScaler()
            scaled_data = scaler.fit_transform(values)
            n_steps = 24
            X, y = split_sequences(scaled_data, n_steps)
            n_features = X.shape[2]
            # Split the data into training and testing sets
            train_size = int(len(df_sorted) * 0.2)
            X_train, X_test = X[train_size:,] , X[:train_size,] 
            # print('X_train' ,X_train.shape)
            # print('X_test' ,X_test.shape)
            Y_train, Y_test = y[train_size:,] , y[:train_size,]
            # print('Y_train' ,Y_train.shape)
            # print('Y_test' ,Y_test.shape)
            n_features = X.shape[2]
            # define model
            model = Sequential()
            model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
            model.add(LSTM(100, activation='relu'))
            model.add(Dense(n_features))
            model.compile(optimizer='adam', loss='mse')
            # fit model
            model.fit(X_train, Y_train, epochs=45, verbose =1 )
            # save the model to disk
            filename = '%s.pkl' % aqsid
            pickle.dump(model, open(filename, 'wb'))
            
            src_bucket.upload_file(filename, f"models/{filename}")

            print('>>>>>>>>>>>>>>>> pickle generation ended for :', aqsid)
