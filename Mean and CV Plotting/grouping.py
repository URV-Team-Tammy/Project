import pandas as pd
import os

# specify the folder path
folder_path = os.path.join(os.path.dirname(__file__), '..\\Data Cleaning\\out2')

# get a list of files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('2023_CI.csv')]

first = True
dfs = pd.DataFrame()

# read each file and create a dataframe
for file in files:
    if first:
        dfs =  pd.read_csv(os.path.join(folder_path, file))
        dfs.set_index('MTU', inplace=True)
        dfs = dfs.rename(columns={"CI_avg": "BE"})
        first = not first
    else:
        region = file[0:2]
        df = pd.read_csv(os.path.join(folder_path, file))
        df.set_index('MTU', inplace=True)
        dfs[region] = df['CI_avg']

# # concatenate the dataframes along the columns (axis=1)
# combined_df = pd.concat(dfs, axis=1)

# # reset the index to create a new column for the time
# combined_df.reset_index(inplace=True)

# # rename the columns to include the region names
# region_names = [f.split('_')[0] for f in files]
# combined_df.columns = ['Time'] + region_names

# save the combined dataframe to a new file
dfs.to_csv('Mean and CV Plotting/combined_regions_2023.csv')