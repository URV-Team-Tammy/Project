import pandas as pd
import os

# specify the folder path
folder_path = 'out2'

# get a list of files in the folder
files = [f for f in os.listdir(folder_path) if f.split('_')[1] == '2022' and f.endswith('.csv')]

# create a list to store the dataframes for each region
dfs = []

# read each file and create a dataframe
for file in files:
    df = pd.read_csv(os.path.join(folder_path, file), names=['MTU', 'CI_avg'])
    df.set_index('MTU', inplace=True)
    dfs.append(df)

# concatenate the dataframes along the columns (axis=1)
combined_df = pd.concat(dfs, axis=1)

# reset the index to create a new column for the time
combined_df.reset_index(inplace=True)

# rename the columns to include the region names
region_names = [f.split('_')[0] for f in files]
combined_df.columns = ['Time'] + region_names

# save the combined dataframe to a new file
combined_df.to_csv('combined_regions_2022.csv', index=False)