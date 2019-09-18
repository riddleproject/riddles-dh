# get metadata about the mapping csv

import pandas as pd
from datetime import datetime

# load up the sheet of data
train = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/custom_locations.csv")

def get_date(item):
    if str(item) == 'nan':
    	return None
    date = datetime.strptime(str(item), '%Y-%m-%d')
    return date


dates = train['Newspaper_Date'].tolist()
dates = [get_date(date) for date in dates]

dates = list(filter(None, dates))
print(max(dates))
print(min(dates))