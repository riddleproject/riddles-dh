# convert csv of geo data into a geojson file encoding the same information

import json
import pandas as pd
from datetime import datetime
import numpy as np

meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-dh/workset/mapping/Complete_Menus.csv")
meta = meta.dropna(subset=['Coordinates', 'Newspaper Issue Date'])


meta = meta.sort_values(by=['Archive'])

def type_to_int(string):
	types = list(meta['Archive'].unique())
	return types.index(string)

def make_coord(coord, archive):
	coordinates = (coord[:-1])[1:].split(',')
	coordinates = [float(coord) for coord in coordinates]
	if (coordinates[0] > -10):
		if archive not in ['British Newspaper Archives', 'Enigmatic Bill of Fare']:
			return None
	if (coordinates[1] < 15):
		return None
	return coordinates

meta['Coordinates'] = meta.apply(lambda row: make_coord(row['Coordinates'],row['Archive']), axis=1)

meta = meta.dropna(subset=['Coordinates', 'Newspaper Issue Date'])


def make_json(row, i):
	coordinates = row['Coordinates']
	date = row['Newspaper Issue Date']
	
	host = str(row['Organization_Hosting'])
	archive = row['Archive']
	if 'LOC' in archive:
		archive = 'Chronicling America'

	has_menu = 0
	if row['MENU'] is not np.nan:
		has_menu = 1

	# The conundrum event took place in [LOCATION], as advertised by [NEWSPAPER] on [DATE]. ([ARCHIVE])
	
	description = '<div style=\'background-color:"#F5F5DC"\'>The Conundrum Event took place in <strong>' + str(row['Location']) +\
				  '</strong>, as advertised by <strong>' + str(row['Newspaper']).title() + '</strong> on <strong>' +date+\
				  '</strong>. (' + str(archive) + ")</div>"
	if has_menu:
		description = '<div style="overflow-y: auto;""><div style=\'background-color:"#F5F5DC"\'>The Conundrum Event took place in <strong>' + str(row['Location']) +\
				  '</strong>, as advertised by <strong>' + str(row['Newspaper']).title() + '</strong> on <strong>' +date+\
				  '</strong>.' +\
				 "<div id=\"menu"+i+"\" style='display:'block';'><br><br>" + str(row['MENU']) + "</div>"+\
				 "<br><br><a href=# onclick=\"showHideMenu('menu"+i+"', 'button"+i+"')\" id='button"+i+"'>Show menu</a></div></div>"
	body = {
		"type": "Feature",
		"properties": {
			"Newspaper": str(row['Newspaper']),
			'Persons': str(row['Persons']),
			"Host": str(host),
			"Location": str(row['Location']),
			'Comments': str(row['Notes']),
			"Year": datetime.strptime(str(date), '%B %d, %Y').year,
			"Type": type_to_int(row['Archive']),
			'has_menu': has_menu,
			'description': str(description)
		},
		"geometry":
		{
			"type":"Point",
			"coordinates": coordinates
		}
	}

	return body

jsons = []
for i,row in meta.iterrows():
	jsons.append(make_json(row, str(i)))


final = {
  "type": "FeatureCollection",
  "features": jsons
  }


path = "/Users/ndrezn/OneDrive - McGill University/Github/riddleproject.github.io/data.geojson"
with open(path, 'w') as outfile:
	json.dump(final, outfile)