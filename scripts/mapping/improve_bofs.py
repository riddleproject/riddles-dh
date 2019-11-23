import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
from os import listdir
from datetime import datetime


file = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/Complete_Menus.csv"

df = pd.read_csv(file).reset_index(drop=True)

def guess_date(string):
	for fmt in ["%B %d, %Y", '%B, %Y', "%B %Y", '%Y-%m-%d', '%d-%b-%y', '%m/%d/%y', '%Y', '%d-%b-%Y']:
		try:
			date = datetime.strptime(string, fmt)
			if date.year >= 2000:
				date -= pd.DateOffset(years=100)
			return date.strftime("%B %d, %Y")
		except ValueError:
			continue
	return np.nan

dates = [str(date) for date in df['Newspaper Issue Date'].tolist()]
dates = [guess_date(date) for date in dates]
df['Newspaper Issue Date'] = dates

print(dates)

def get_loc(place, coordinates, n):
	if coordinates is np.nan:    
		if place is np.nan or n==0:
			return None
		try:
			location = geolocator.geocode(place)
			if location is None:
				return None

			coordinates = [location.longitude, location.latitude] 
		except:
			return get_loc(place, coordinates, n-1)
	return coordinates

print("Getting coordinates.")
geolocator = Nominatim(user_agent='doodad')
# df['Coordinates'] = df.apply((lambda row:get_loc(row['Location'], row['Coordinates'],5)), axis=1)


df.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/Complete_Menus.csv")
