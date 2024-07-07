import yaml

with open('defaults.yaml','r') as f:
    defaults = yaml.safe_load(f)
    defaults = defaults['emissionFactors']['lifecycle']

with open('ES.yaml','r') as f:
    data_ES = yaml.safe_load(f)
    data_ES = data_ES['emissionFactors']['lifecycle']

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
    print(res)
    return res

extract_ci(data_ES,defaults)