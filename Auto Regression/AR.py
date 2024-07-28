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

def join_csv(region):
    joined_files = os.path.join("./", region+"*.csv") 
    joined_list = sorted(glob.glob(joined_files))
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
    df["MTU"] = pd.to_datetime(df["MTU"],infer_datetime_format=True)
    df.set_index("MTU", inplace=True)
    return df.dropna()

df = join_csv("BE")
# start = pd.to_datetime("2023-07-01 00:00:00")
# df = df[start:]

dftest = adfuller(df['CI_avg'], autolag = 'AIC') # Stationary Test : P-Value < 0.5
print("P-Value : ",dftest[1])

plt.figure(figsize = (30,4))
plt.plot(df.CI_avg)
plt.title('Average Carbon Intensity over Time',fontsize = 20)
plt.ylabel('Average Carbon Intensity',fontsize = 16)

acf_plot = plot_acf(df,lags=100)

pacf_plot = plot_pacf(df)

plt.show()

# Experiment 1 : Predicting 2023 after training on df from 2017-2022.

train_end = pd.to_datetime("2022-12-31 23:00:00")
test_end = pd.to_datetime("2023-12-31 23:00:00")

train_data = df[:train_end]
test_data = df[train_end + datetime.timedelta(hours = 1):test_end]

model = AutoReg(train_data,lags = 1000)

model_fit = model.fit()
print(model_fit.summary())

predictions = model_fit.predict(start = train_data.shape[0] , end = df.shape[0]-1, dynamic = False)
test_data['Prediction'] = predictions.values
final_df = test_data

rmse = sqrt(mean_squared_error(final_df.CI_avg,final_df.Prediction))
print(rmse) 

plt.plot(final_df.CI_avg)
plt.plot(final_df.Prediction, color = "red")
plt.show()

# Experiment 2 : Predicting future after training on entire df.

def predict_future(df,years):
    model = AutoReg(df,lags = 100)

    model_fit = model.fit()
    # print(model_fit.summary())

    timestamp_list = [df.index[-1] + datetime.timedelta(hours = x) for x in range(1,years*366*24+1)] 

    predictions_future = model_fit.predict(start = df.shape[0]+1 , end = df.shape[0]+years*366*24, dynamic = False)

    predict_df = pd.DataFrame()
    predict_df['MTU'] = timestamp_list
    predict_df['CI_avg'] = predictions_future.values
    predict_df.set_index("MTU", inplace=True)

    return predict_df

print(predict_future(df,1))


