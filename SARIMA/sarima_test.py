import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from statsmodels.tsa.statespace.sarimax import SARIMAX 
import os 
from statsmodels.tsa.stattools import adfuller 
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf 

def open_csv(region):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../Data Cleaning/out3/'+region+'_sum.csv'))
    df["MTU"] = pd.to_datetime(df["MTU"],infer_datetime_format=True)
    df.set_index("MTU", inplace=True)
    df = df.drop('Unnamed: 0', axis=1)
    return df.dropna()

def check_stationarity(df): 
    # Perform the Dickey-Fuller test 
    result = adfuller(df, autolag='AIC') 
    p_value = result[1] 
    print(f'ADF Statistic: {result[0]}') 
    print(f'p-value: {p_value}') 
    print('Stationary' if p_value < 0.05 else 'Non-Stationary') 

def sarima_test(df):
    train_size = int(len(df) * 0.8)
    train, test = df[:train_size], df[train_size:]

    p, d, q = 1, 1, 1
    P, D, Q, s = 1, 1, 1, 12
    
    model = SARIMAX(train, order=(p, d, q), seasonal_order=(P, D, Q, s)) 
    results = model.fit() 
    print(results.summary())
    
    # Forecast
    forecast = results.get_forecast(steps=len(test))

    # Get the predicted values
    predicted_values = forecast.predicted_mean

    plt.figure(figsize=(10, 6))
    plt.plot(train, label='Training Data')
    plt.plot(test, label='Actual Data')
    plt.plot(predicted_values, label='Predicted Data', color='red')

    plt.legend()
    plt.show()

    df['Prediction'] = forecast.values
  

df = open_csv("BE")  
# check_stationarity(df['CI_avg']) -- this is slow, it's stationary 


sarima_test(df['CI_avg'])