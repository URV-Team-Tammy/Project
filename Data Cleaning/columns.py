import pandas as pd
from datetime import datetime

df = pd.read_csv("AT_2021.csv")

def extract_month(df,month):
    time = list(df['MTU'].values)
    res = []
    for t in time:
        date_string = t.strip().split(' ')[0]
        date = datetime.strptime(date_string, '%d.%m.%Y')
        if date.month == month:
            res.append(t)
    return res

jan_df = df[df['MTU'].isin(extract_month(df,1))]

print(jan_df.info())