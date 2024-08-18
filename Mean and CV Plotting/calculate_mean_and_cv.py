import pandas as pd 
import os
import sys

def format_df(df): 
    copy_df = df.copy(deep=True)
    copy_df['MTU'] = copy_df['MTU'].str.slice(stop=-6)
    copy_df['MTU'] = pd.to_datetime(copy_df['MTU'])
    copy_df = copy_df.bfill().ffill()
    return copy_df

def get_year_df(df, selected_year = 2022, drop_datetime=True): 
    copy_df = format_df(df)

    copy_df = copy_df[copy_df['MTU'].dt.year == selected_year]
    if drop_datetime: 
        copy_df.drop(columns=['MTU'], inplace=True)
        copy_df.reset_index(drop=True, inplace=True)

    return copy_df


carbon_df = pd.read_csv("combined_regions_2023.csv")

year = 2023

year_df = pd.DataFrame(columns=["mean", "cv"])

raw_year_df = get_year_df(carbon_df, year, drop_datetime=False)

print(raw_year_df)

raw_year_df.set_index('MTU', inplace=True)
raw_year_df.index = pd.to_datetime(raw_year_df.index)

grouped_year_df = raw_year_df.groupby(raw_year_df.index.date) # group by date

region_daily_std = grouped_year_df.std()
region_daily_mean = grouped_year_df.mean()

region_year_mean = raw_year_df.mean()
region_year_cv = (region_daily_std/region_daily_mean).mean()

year_df['mean'] = region_year_mean
year_df['cv'] = region_year_cv

year_df.index.name = 'zone_code'

year_df.to_csv(f'mean_and_cv_{year}.csv')
