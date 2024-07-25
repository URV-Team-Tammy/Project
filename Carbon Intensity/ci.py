import yaml
import os
import sys
import glob
import pandas as pd

#output_name = sys.argv[1]
folder_name = sys.argv[1]

with open('defaults.yaml','r') as f:
    defaults = yaml.safe_load(f)
    defaults = defaults['emissionFactors']['lifecycle']

#with open('ES.yaml','r') as f:
  #  data_ES = yaml.safe_load(f)
    #data_ES = data_ES['emissionFactors']['lifecycle']

def extract_ci(data,defaults):
    sources = ['biomass','coal','gas','geothermal','hydro','nuclear','oil','solar','wind','unknown','battery discharge','hydro discharge']
    res = {}
    for s in sources:
        if s in data:
            if type(data[s]) == list:
                res[s] = data[s][-1]['value']
            else:
                res[s] = data[s]['value']
        else:
            res[s] = defaults[s]['value']
    # print(res)
    return res

ci_data = {}
for filename in glob.glob(os.path.join(folder_name, '*.yaml')):
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        data = data['emissionFactors']['lifecycle']
        region = os.path.basename(filename).replace('.yaml', '')
        # ci_data[region] = extract_ci(data, defaults)
        ci_data[region] = list(extract_ci(data, defaults).values())

df = pd.DataFrame.from_dict(ci_data,orient='index', columns=["battery discharge", "biomass", "coal", "gas", "geothermal", "hydro", "hydro discharge", "nuclear", "oil", "solar", "unknown", "wind"])
df.index.names = ['region']
df.to_csv("output.csv")

# with open('output.yaml', 'w') as f:
    # yaml.dump(ci_data, f)
#extract_ci(data_ES,defaults)
#accept from commandline name of folder 
#-> get file in folder in a líst 
#-> run for in that list like extract ci 