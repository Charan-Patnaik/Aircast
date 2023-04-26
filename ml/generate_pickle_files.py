import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.layers import Dense, Dropout,LSTM
import pickle
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, DateTime
import boto3
import boto3.s3
import botocore
from dotenv import load_dotenv
import os

load_dotenv()

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_SECRET')
# AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')

## Importing 1 year data
engine = create_engine('mysql+pymysql://admin:123456789@aircast.cjisewdv5jgk.us-east-1.rds.amazonaws.com:3306/aircast')
# not in S3
# my_list = ['300270006', '300290009', '300290049', '300298001', '300310019', '300490026', '300530018', '300630024', '300710010', '300750001', '300810007', '300830002', '300890007', '300930005', '301110066', '301110087', '310250002', '310550053', '310550056', '311079991', '311090016', '311090022', '311530007', '320010002', '320030024', '320030043', '320030044', '320030071', '320030298', '320030299', '320030540', '320030561', '320031501', '320050007', '320070005', '320190006', '320230014', '320230015', '320310020', '320310025', '320311005', '320311007', '320311026', '320312002', '320312009', '320330101', '325100020', '330012004', '330050007', '330074002', '330090010', '330111011', '330115001', '330131006', '330150014']
# in s3
# my_list = ['340010006', '340030006', '340030010', '340070002', '340110007', '340150002', '340170006', '340171002', '340171003', '340190001', '340210005', '340219991', '340230011', '340250005', '340273001', '340290006', '340315001', '340390004', '340392003', '340410007', '350010023', '350010026', '350010029', '350011012', '350011013', '350130008', '350130016', '350130019', '350130020', '350130021']
my_list = ['350130022', '350130023', '350130024', '350130025', '350151005', '350250008', '350290003', '350431001', '350450009', '350450018', '350451005', '350490021', '350550005', '350610008', '360010012', '360050080', '360050110', '360050133', '360270007', '360290002', '360290023', '360291014', '360310003', '360410005', '360450002', '360470052', '360550015', '360590005', '360610115', '360610135', '360631006', '360671015', '360710002', '360750003', '360790005', '360810120', '360810124', '360810125', '360850111', '360870005', '360910004', '361010003', '361030002', '361030004', '361030009', '361099991', '361173001', '361192004', '370110002', '370130151', '370210030', '370210034', '370270003', '370319991', '370330001', '370350004', '370510009', '370510010', '370570002', '370630015', '370630099', '370650099', '370670022', '370670030', '370671008', '370750001', '370770001', '370810013', '370870008', '370870013', '370870035', '370870036', '371010002', '371070004', '371090004', '371139991', '371170001', '371190041', '371190045', '371190046', '371210004', '371230001', '371239991', '371290002', '371310003', '371450003', '371470006', '371570099', '371590021', '371730002', '371790003', '371830014', '371990004', '380130004', '380150003', '380171004', '380570004', '380650002', '381010003', '390030009', '390071001', '390130006', '390170018', '390170019', '390170020', '390170021', '390170023', '390179991', '390230001', '390230003', '390230005', '390250022', '390271002', '390350034', '390350038', '390350060', '390350064', '390350065', '390355002', '390410002', '390490038', '390490081', '390530006', '390550004', '390570006', '390610006', '390610010', '390610040', '390610048', '390810017', '390830003', '390850003', '390850007', '390870011', '390870012', '390890005', '390890008', '390930018', '390950024', '390950027', '390950035', '390970007', '391030004', '391090005', '391130038', '391150004', '391219991', '391331001', '391351001', '391510016', '391510020', '391510022', '391514005', '391530017', '391550011', '391550013', '391550014', '391670004', '391730003', '400170101', '400190297', '400270049', '400310651', '400370144', '400430860', '400470555', '400979014', '401050207', '401090097', '401091037', '401130226', '401210415', '401359021', '401430174', '401430175', '401430178', '401431127', '410170120', '410230002', '410290201', '410290203', '410390059', '410390060', '410430104', '410432003', '410470004', '410470007', '410470123', '410610120', '410670005', '420010001', '420030008', '420030064', '420030067', '420031008', '420050001', '420070005', '420070014', '420110011', '420130801', '420150011']
# aqsid = '250250042'

session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id='AKIAY5JK22NETTJWNQ46',
    aws_secret_access_key='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')

s3 = session.resource('s3')

src_bucket = s3.Bucket('damg-aircast')


# %%s

for aqsid in my_list:

	####

	#####################   DATA EXTRACTION FROM AWS DataBase #############################

	####
	# Read data from the SQL table into a dataframe
	print('>>>>>>>>>>>>>>>>  data extraction started')
	inp_data = pd.read_sql_query('SELECT * from aircast.StationsData WHERE aquid = "%s"' % aqsid, engine)
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

	# s3 bucket file upload
	src_bucket.upload_file(filename, f"models/{filename}")


	print('>>>>>>>>>>>>>>>> pickle generation ended for :', aqsid)




# %%
