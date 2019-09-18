import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


path = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/complete csvs/"
paths = [f for f in listdir(path) if isfile(join(path, f))]
paths.pop(0)
csvs = [pd.read_csv(path+f) for f in paths]

meta = pd.concat(csvs, sort=False)


def guess_date(string):
    for fmt in ["%B %d, %Y", "%B %Y", '%Y-%m-%d', '%d-%b-%y']:
        try:
            return datetime.strptime(string, fmt)
        except ValueError:
            continue
    return None


meta=meta.dropna(axis=1,how='all')
meta = meta.dropna(how='all')
dates = [str(date) for date in meta['Date'].tolist()]
dates = [guess_date(date) for date in dates]
meta['Date'] = dates

meta.loc[meta['Date'].dt.year >= 2000, 'Date'] -= pd.DateOffset(years=100)

meta = meta.sort_values('Date')
meta = meta.dropna(subset=['Date'])

meta.reset_index(drop=True)

def location_combiner(city, state, country, location):
	if location is np.nan:
		return str(city) + ", " + str(state) + ", " + str(country)
	else:
		return location

# meta['Location']=meta.City.astype(str).str.cat(meta[['State/Province','Location']].astype(str),na_rep='', sep=' ')
meta['Location'] = meta.apply(lambda row: location_combiner(row['City'],row['State/Province'], row['Country'],row['Location']), axis=1)

print(meta['Location'])

meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete.csv")

def make_coord(string):
	coordinates = (string[:-1])[1:].split(',')
	coordinates = [float(coord) for coord in coordinates]
	coordinates =  list(reversed(coordinates))
	return coordinates

dates = [str(date) for date in meta['Date'].tolist()]
dates = [guess_date(date) for date in dates]
meta['Date'] = dates


meta = meta.dropna(subset=['Coordinates', 'Date'])
meta = meta.reset_index()
meta = meta.sort_values('Date')
print(meta['Date'])

exit()


meta['Coordinates'] = meta['Coordinates'].apply(make_coord)


def type_to_int(string):
	if string == 'Supper':
		return 0
	if string == 'North American Supper':
		return 1
	if string == 'Tea':
		return 2
	if string == 'Social':
		return 3

def fix_type(string):
	if string == 'Supper':
		return 'LOC supper'
	if string == 'North American Supper':
		return 'supper'
	else:
		return string.lower()

meta = meta.fillna('n/a')

def make_json(row):
	coordinates = row['Coordinates']
	
	date = row['Date']

	if row['Type'] == 'North American Supper':
		location = str(row['City']) + ", " + str(row['State/Province'])
	else:
		location = row['Publisher']
	
	host = str(row['Organization_Hosting'])

	description = 'This conundrum ' + fix_type(row['Type']) + ' was published in <strong>' + str(location) +\
				  '</strong> by <strong>' + str(row['Newspaper']).title() + "</strong> on <strong>" + str(date.strftime('%B %d, %Y')) + "</strong>."
	
	body = {
		"type": "Feature",
		"properties": {
			"Newspaper": row['Newspaper'],
			'Persons': row['Persons'],
			"Host": host,
			"Location": location,
			'Comments': row['Aditional_Comments'],
			"Year": date.year,
			"Type": type_to_int(row['Type']),
			'description': description
		},
		"geometry":
		{
			"type":"Point",
			"coordinates": coordinates
		}
	}

	return body

jsons = []
for index,row in meta.iterrows():
	jsons.append(make_json(row))


final = {
  "type": "FeatureCollection",
  "features": jsons
  }


path = "/Users/ndrezn/OneDrive - McGill University/Github/nathaliecookehathi.github.io/data/map_data_all.geojson"
with open(path, 'w') as outfile:
	json.dump(final, outfile)