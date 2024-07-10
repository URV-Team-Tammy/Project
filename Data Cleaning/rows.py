

import pandas as pd
from datetime import datetime


def parsing_custom_timestamp(timestamp):
    start_time_str = timestamp.split(' - ')[0]
    start_time = datetime.strptime(start_time_str, '%d.%m.%Y %H:%M')
    return start_time


df = pd.read_csv('AT_2021.csv') #Read the CSV file


df['MTU'] = df['MTU'].apply(parsing_custom_timestamp) #Applying the timestamp settings


df.set_index('MTU', inplace=True)


df = df.apply(pd.to_numeric, errors='coerce')


df_resampled = df.resample('H').sum()

df_tofill = df_resampled.fillna(method='ffill')

df_tofill.reset_index(inplace=True)

df_tofill.to_csv('new_hourly_mean_new.csv', index=False)

print(df_tofill)





