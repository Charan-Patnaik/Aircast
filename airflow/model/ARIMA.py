#%%
import pandas as pd
#from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import urllib.request
import os

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
    return forecast['datetime'], forecast['value']

