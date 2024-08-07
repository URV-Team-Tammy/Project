import datetime
import glob 
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
from time import time

def open_csv(region):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../Data Cleaning/out3/'+region+'_sum.csv'))
    df["MTU"] = pd.to_datetime(df["MTU"],infer_datetime_format=True)
    df.set_index("MTU", inplace=True)
    df = df.drop('Unnamed: 0', axis=1)
    return df.dropna()

df = open_csv("BE")
# print(df)
# start = pd.to_datetime("2023-07-01 00:00:00")
# df = df[start:]

def test_df(df):
    dftest = adfuller(df['CI_avg'], autolag = 'AIC') # Stationary Test : P-Value < 0.5
    print("P-Value : ",dftest[1])

    plt.figure(figsize = (30,4))
    plt.plot(df.CI_avg)
    plt.title('Average Carbon Intensity over Time',fontsize = 20)
    plt.ylabel('Average Carbon Intensity',fontsize = 16)

    acf_plot = plot_acf(df,lags=100)

    pacf_plot = plot_pacf(df)

    plt.show()

    return

test_df(df)

# Experiment 1 : Predicting 2023 after training on df from 2017-2022.

def test_error(df,train_end,test_end):
    train_data = df[:train_end]
    test_data = df[train_end + datetime.timedelta(hours = 1):test_end]
    # print(train_data)
    # print(test_data)

    model = AutoReg(train_data,lags = 147)

    model_fit = model.fit()
    # print(model_fit.summary())

    predictions = model_fit.predict(start = train_data.shape[0] , end = train_data.shape[0] + test_data.shape[0]-1, dynamic = False)
    test_data['Prediction'] = predictions.values
    final_df = test_data
    print(final_df)

    rmse = sqrt(mean_squared_error(final_df.CI_avg,final_df.Prediction))
    print(rmse) 

    plt.plot(final_df.CI_avg)
    plt.plot(final_df.Prediction, color = "red")
    plt.show()

    return

test_error(df,pd.to_datetime("2017-1-31 23:00:00"),pd.to_datetime("2017-3-1 23:00:00"))

# Experiment 2 : Predicting future after training on entire df.

def predict_future_1(df,years):
    df = df[-31*24:]
    timestamp_list = [df.index[-1] + datetime.timedelta(hours = x) for x in range(1,years*366*24+1)] 
    final_df = pd.DataFrame()

    while timestamp_list:
        if len(timestamp_list) < 31*24:
            curr_time = timestamp_list
            timestamp_list = []
        else:
            curr_time = timestamp_list[:31*24]
            timestamp_list = timestamp_list[31*24:]
        
        model = AutoReg(df,lags = 147)
        model_fit = model.fit()
        # print(model_fit.summary())    

        predictions_future = model_fit.predict(start = df.shape[0]+1 , end = df.shape[0]+len(curr_time), dynamic = False)

        predict_df = pd.DataFrame()
        predict_df['MTU'] = curr_time
        predict_df['CI_avg'] = predictions_future.values
        predict_df.set_index("MTU", inplace=True)
        final_df = pd.concat([final_df,predict_df])
        df = predict_df

    return final_df

def predict_future_2(df,years):
    df = df[-31*24:]
    print(df)
    timestamp_list = [df.index[-1] + datetime.timedelta(hours = x) for x in range(1,years*366*24+1)] 
    
    model = AutoReg(df,lags = 150)
    model_fit = model.fit()
    # print(model_fit.summary())    

    predictions_future = model_fit.predict(start = df.shape[0]+1 , end = df.shape[0]+years*366*24, dynamic = False)

    predict_df = pd.DataFrame()
    predict_df['MTU'] = timestamp_list
    predict_df['CI_avg'] = predictions_future.values
    predict_df.set_index("MTU", inplace=True)

    return predict_df

print(predict_future_1(df,2))
print(predict_future_2(df,2))


