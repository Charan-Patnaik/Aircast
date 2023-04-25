#%%
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.layers import Dense, Dropout,LSTM
import pickle


def generating_pickle_files_all_sites():
	#%%
	## Importing 1 year data
	# print('>>>>>>>>>>>>>>>>  data extraction started')
	filename = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/combine_data.csv'
	inp_data =  pd.read_csv(filename, sep = ",")
	# print('>>>>>>>>>>>>>>>>  data extraction done')

	#%%
	## Preprocessing
	# droping null values
	inp_data = inp_data.dropna()

	# Select the last row
	last_row = inp_data.iloc[-1]

	# Drop the last row
	inp_data.drop(last_row.name, inplace=True)

	# Check if the hour column contains valid date format
	mask = inp_data['hour'].str.contains('^\d{2}:\d{2}$')

	# Filter out rows with invalid date formats
	inp_data = inp_data[mask]

	## Filter by AQSID
	aqsid = '250250042'
	inp_data['AQSID'] = inp_data['AQSID'].astype(str)
	site_data = inp_data[inp_data['AQSID'] == aqsid].reset_index(drop = True)
	print('>>>>>>>>>>>>>>>>  site data pull done')
	####

	##################    FEATURE ENGINEERING  #############################

	####

	###### Droping unrequired columns
	site_df = site_data.copy()
	site_df = site_df.drop(columns = ['AQSID','sitename','GMT offset','reporting units','datasource'])

	## Creating datetime stamp column from input
	site_df['datetime'] = pd.to_datetime(site_df.date.astype(str) + ' ' + site_df.hour.astype(str) + ':00')
	site_df['datetime'] = pd.to_datetime(site_df['datetime'])

	## Drop unrequired columns
	site_df.drop(columns = ['date','hour'])
	# Rearrange the columns
	site_df = site_df[['datetime','parameter name','value']]

	## Creating df's for required major pollutants
	no2_df = pd.DataFrame()
	pm25_df = pd.DataFrame()
	pm10_df = pd.DataFrame()
	co_df = pd.DataFrame()
	ozone_df = pd.DataFrame()
	so2_df = pd.DataFrame()
	if 'NO2' in site_df['parameter name'].unique():
		no2_df = site_df[site_df['parameter name'] == 'NO2'].reset_index(drop=True)
	if 'PM2.5' in site_df['parameter name'].unique():
		pm25_df = site_df[site_df['parameter name'] == 'PM2.5'].reset_index(drop=True)
	if 'PM10' in site_df['parameter name'].unique():
		pm10_df = site_df[site_df['parameter name'] == 'PM10'].reset_index(drop=True)
	if 'CO' in site_df['parameter name'].unique():
		co_df = site_df[site_df['parameter name'] == 'CO'].reset_index(drop=True)
	if 'OZONE' in site_df['parameter name'].unique():
		ozone_df = site_df[site_df['parameter name'] == 'OZONE'].reset_index(drop=True)
	if 'SO2' in site_df['parameter name'].unique():
		so2_df = site_df[site_df['parameter name'] == 'SO2'].reset_index(drop=True)


	### Combining the segregated pollutant data together:
	req_df = pd.DataFrame()
	temp_df = pd.DataFrame()
	for i in ['NO2','SO2','OZONE','CO','PM10','PM2.5']:
		if i in site_df['parameter name'].unique():
			temp_df = site_df[site_df['parameter name'] == i ].reset_index(drop=True)
			req_df = pd.concat([req_df, temp_df]).reset_index(drop = True)

	# Create the new dataframe with datetime as the index, parameter as the columns, and values as the cells
	req_pivot = req_df.pivot_table(index='datetime', columns='parameter name', values='value')
	## Sorting
	df_sorted = req_pivot.sort_values(by='datetime')
	## Droping null values
	df_sorted = df_sorted.dropna()

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

	print('>>>>>>>>>>>>>>>> pickle generation ended for :', aqsid)




# %%
