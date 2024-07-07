import pandas as pd
from datetime import datetime


def parsing_custom_timestamp(timestamp):
    start_time_str = timestamp.split(' - ')[0]
    start_time = datetime.strptime(start_time_str, '%d.%m.%Y %H:%M')
    return start_time


def extract_month(df,month):
    time = list(df['MTU'].values)
    res = []
    for t in time:
        date_string = t.strip().split(' ')[0]
        date = datetime.strptime(date_string, '%d.%m.%Y')
        if date.month == month:
            res.append(t)
    return res

# in df out df2
def merge_columns(df, df2):
    biomass = "Biomass  - Actual Aggregated [MW]"
    coal = "Fossil Brown coal/Lignite  - Actual Aggregated [MW]"
    coal_gas = "Fossil Coal-derived gas  - Actual Aggregated [MW]"
    gas = "Fossil Gas  - Actual Aggregated [MW]"
    hard_coal = "Fossil Hard coal  - Actual Aggregated [MW]"
    oil = "Fossil Oil  - Actual Aggregated [MW]"
    oil_shale = "Fossil Oil shale  - Actual Aggregated [MW]"
    peat = "Fossil Peat  - Actual Aggregated [MW]"
    geo_thermal = "Geothermal  - Actual Aggregated [MW]"
    hydro_pumped = "Hydro Pumped Storage  - Actual Aggregated [MW]"
    hydro_pumped_consumption = "Hydro Pumped Storage  - Actual Consumption [MW]"
    hydro_run = "Hydro Run-of-river and poundage  - Actual Aggregated [MW]"
    hydro_reservoir = "Hydro Water Reservoir  - Actual Aggregated [MW]"
    marine = "Marine  - Actual Aggregated [MW]"
    nuclear = "Nuclear  - Actual Aggregated [MW]"
    other = "Other  - Actual Aggregated [MW]"
    other_renewable = "Other renewable  - Actual Aggregated [MW]"
    solar = "Solar  - Actual Aggregated [MW]"
    waste = "Waste  - Actual Aggregated [MW]"
    wind_offshore = "Wind Offshore  - Actual Aggregated [MW]"
    wind_onshore = "Wind Onshore  - Actual Aggregated [MW]"

    df2['Biomass'] = df[biomass]
    df2['Coal'] = df[coal] + df[peat] + df[hard_coal]
    df2['Gas'] = df[gas] + df[coal_gas]
    df2['Oil'] = df[oil] + df[oil_shale]
    df2['Geothermal'] = df[geo_thermal]
    df2['Hydro'] = df[hydro_pumped] + df[hydro_reservoir] + df[hydro_run]
    df2['Marine'] = df[marine]
    df2['Unknown'] = df[other] + df[other_renewable]
    df2['Solar'] = df[solar]
    df2['Nuclear'] = df[nuclear]
    df2['Waste'] = df[waste]
    df2['Wind'] = df[wind_offshore] + df[wind_onshore]


def ne_to_zero(df):
    return df.fillna(0)


df = pd.read_csv('BE_2021.csv') #Read the CSV file

# Rows
df['MTU'] = df['MTU'].apply(parsing_custom_timestamp) #Applying the timestamp settings
df.set_index('MTU', inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')
df_resampled = df.resample('H').mean()
df_tofill = df_resampled.fillna(method='ffill')
df_tofill.reset_index(inplace=True)

# Columns
df_tofill = ne_to_zero(df_tofill)
df_AT_merged = pd.DataFrame()
merge_columns(df_tofill, df_AT_merged)

# Test
print(df_tofill.info())
print(df_AT_merged.info())
print(df_AT_merged)

df_AT_merged.to_csv('BE_2021_Clean.csv', index=False)




