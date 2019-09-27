import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join
import time
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


path = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/complete csvs/"
paths = [f for f in listdir(path) if isfile(join(path, f))]
paths.pop(0)
csvs = [pd.read_csv(path+f) for f in paths]

meta = pd.concat(csvs, sort=False)


def guess_date(string):
    for fmt in ["%B %d, %Y", "%B %Y", '%Y-%m-%d', '%d-%b-%y', '%m/%d/%y']:
        try:
            date = datetime.strptime(string, fmt)
            if date.year >= 2000:
            	date -= pd.DateOffset(years=100)
            return date.strftime("%B %d, %Y")
        except ValueError:
            continue
    return np.nan


meta=meta.dropna(axis=1,how='all')
meta = meta.dropna(how='all')
dates = [str(date) for date in meta['Date'].tolist()]
dates = [guess_date(date) for date in dates]
meta['Date'] = dates

# meta.loc[meta['Date'].dt.year >= 2000, 'Date'] -= pd.DateOffset(years=100)

meta = meta.sort_values('Date')
meta = meta.sort_values('Archive')

def location_combiner(city, state, county, country, location):
	city = str(city).replace("(?)", "")
	if country == 'England':
		if city is np.nan:
			return str(county) + ", " + str(country)
		elif county is np.nan:
			return str(city) + ", " + str(country)
		return str(city) + ", " + str(county) + ", " + str(country)
	
	elif location is np.nan:
		if city is np.nan:
			return str(state) + ", " + str(country)
		elif state is np.nan:
			return str(city) + str(country)
		elif country is np.nan:
			return None
		return str(city) + ", " + str(state) + ", " + str(country)
	
	return location.replace("(?)", "")

def two_comb(d1, d2):
	if d1 is np.nan:
		return d2
	return d1


meta['Location'] = meta.apply(lambda row: location_combiner(row['City'],row['State/Province'], row['County'], row['Country'],row['Location']), axis=1)
meta['Event_Date'] = meta.apply(lambda row: two_comb(row['Event Date'],row['Event_Date']), axis=1)
meta['Notes'] = meta.apply(lambda row: two_comb(row['Aditional_Comments'],row['Notes']), axis=1)

del meta['City']
del meta['State/Province']
del meta['County']
del meta['Country']
del meta['Event Date']
del meta['Reference Type.1']
del meta['Unnamed: 0']
del meta['Aditional_Comments']

meta = meta.reindex(sorted(meta.columns), axis=1)

meta = meta.reset_index(drop=True)

def get_loc(place, n):
    if n == 0:
        return None
    try:
        location = geolocator.geocode(place)
        if location is None:
            return None

        coord = [location.longitude, location.latitude] 
        print(coord)
        return coord
    except:
        return get_loc(place, n-1)


geolocator = Nominatim(user_agent='doodad')
meta['Coordinates'] = meta.apply((lambda row:get_loc(row['Location'],10)), axis=1)

meta = meta.reindex(sorted(meta.columns), axis=1)

meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete_W.csv")
