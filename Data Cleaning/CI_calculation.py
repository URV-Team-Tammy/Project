import pandas as pd
import sys
import os


COLUMNS = ["Biomass","Coal","Gas","Geothermal","Hydro","Hydro Discharge","Nuclear","Oil","Solar","Unknown","Wind"]

if(len(sys.argv) != 2):
    print("usage: python3 cleaner.py filename")
    exit()

filename = sys.argv[1]

df_carbon = pd.read_csv("../Carbon Intensity/carbon_emission_factor_t.csv").set_index("Energy Type")

def CI_calculation(row):
    carbon_emission = total_consumption = 0
    for col in COLUMNS:
        carbon_emission += row[col] * df_carbon.at[col, region]
        total_consumption += row[col]
    return carbon_emission/total_consumption

region = os.path.basename(filename)[0:2]

df = pd.read_csv(filename) #Read the CSV file

df['CI_avg'] = df.apply(CI_calculation,axis=1)

df2 = pd.DataFrame()
df2["MTU"] = df["MTU"]
df2["CI_avg"] = df["CI_avg"]

df2.to_csv("out2/" + os.path.basename(filename)[:-10] + "_CI.csv", index=False)

# file_list = [f for f in os.listdir("out") if os.path.isfile(os.path.join("out", f))][:70]

# for file in file_list:
#     try:
#         filename = "out/" + file

#         region = os.path.basename(filename)[0:2]

#         df = pd.read_csv(filename) #Read the CSV file

#         df['CI_avg'] = df.apply(CI_calculation,axis=1)

        # df2 = pd.DataFrame()
        # df2["MTU"] = df["MTU"]
        # df2["CI_avg"] = df["CI_avg"]

#         df2.to_csv("out2/" + os.path.basename(filename)[:-10] + "_CI.csv", index=False)
#     except ():
#         pass