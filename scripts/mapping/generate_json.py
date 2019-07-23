import pandas as pd
import json
from datetime import datetime


meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/custom_locations.csv")
meta = meta.dropna(subset=['Coordinates', 'Newspaper_Date'])



def make_json(row):
	coordinates = row['Coordinates'][:-1]
	coordinates = coordinates[1:]
	coordinates = coordinates.split(',')
	coordinates = [float(coord) for coord in coordinates] 
	
	date = datetime.strptime(str(row['Newspaper_Date']), '%Y-%m-%d')
	
	body = {
		"type": "Feature",
		"properties": {
			"Host": row['Organization_Hosting'],
			"Month": date.month,
			"Day": date.day,
			"Year": date.year,
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


path = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/map_data.json"
with open(path, 'w') as outfile:
	json.dump(final, outfile)