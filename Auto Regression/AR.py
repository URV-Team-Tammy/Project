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

# df = open_csv("IE")
df = open_csv("PL")
# df = open_csv("NO4")

# print(df)

def test_df(df):
    dftest = adfuller(df['CI_avg'], autolag = 'AIC') # Stationary Test : P-Value < 0.5
    print("P-Value : ",dftest[1])
    print(dftest[1] < 0.5)

    plt.figure(figsize = (30,4))
    plt.plot(df.CI_avg)
    plt.title('Average Carbon Intensity over Time',fontsize = 20)
    plt.ylabel('Average Carbon Intensity',fontsize = 16)

    acf_plot = plot_acf(df,lags=110)
    pacf_plot = plot_pacf(df,lags=110)
    
    plt.savefig("Result_PACF.png" , dpi=300)
    plt.show()

    return

# test_df(df)

# Experiment : Predicting 2023 after training on df from 2017-2022.

def predict_future(df,years,name):
    interval = 1*120*24
    df = df[-interval:]
    timestamp_list = [df.index[-1] + datetime.timedelta(hours = x) for x in range(1,years*366*24+1)] 
    final_df = df

    while timestamp_list:
        if len(timestamp_list) < interval:
            curr_time = timestamp_list
            timestamp_list = []
        else:
            curr_time = timestamp_list[:interval]
            timestamp_list = timestamp_list[interval:]
        
        model = AutoReg(df,lags = 100)
        model_fit = model.fit()

        predictions_future = model_fit.predict(start = df.shape[0]+1 , end = df.shape[0]+len(curr_time), dynamic = False)

        predict_df = pd.DataFrame()
        predict_df['MTU'] = curr_time
        predict_df['CI_avg'] = predictions_future.values
        predict_df.set_index("MTU", inplace=True)
        final_df = pd.concat([final_df,predict_df])
        df = predict_df
    
    plt.figure(figsize = (7,4))
    plt.plot(final_df.CI_avg)
    plt.title('Average Carbon Intensity in '+str(years)+" years for region "+name)
    plt.ylabel('Average Carbon Intensity')
    plt.xlabel('Time')
    plt.savefig("Result_"+name+".png" , dpi=300)
    plt.show()

    return final_df

def test_predict_2023(df):
    last_year = df[pd.to_datetime("2023-01-01 00:00:00"):pd.to_datetime("2023-12-31 23:00:00")]
    df = df[:pd.to_datetime("2022-12-31 23:00:00")]
    predict_last_year = predict_future(df,1)[:pd.to_datetime("2023-12-31 23:00:00")]
    last_year['Prediction'] = predict_last_year['CI_avg']
    rmse = sqrt(mean_squared_error(last_year.CI_avg,last_year.Prediction))
    print(rmse) 

    # plt.plot(last_year.CI_avg[:"2023-01-15 23:00:00"])
    # plt.plot(last_year.Prediction[:"2023-01-15 23:00:00"], color = "red")
    # plt.show()

    return last_year

# test_predict_2023(df)

print(predict_future(df,1,"PL"))

