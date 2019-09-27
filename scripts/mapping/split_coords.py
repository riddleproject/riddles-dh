import pandas as pd
import numpy as np

meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete.csv")
meta=meta.dropna(axis=1,how='all')


def make_coord(coord, archive):
	if coord is np.nan or coord is None:
		return None
	coordinates = (coord[:-1])[1:].split(',')
	coordinates = [float(coord) for coord in coordinates]
	if (coordinates[0] > -10):
		if archive != 'British Newspaper Archives':
			return None
	if (coordinates[1] < 15):
		return None
	return [coordinates[1], coordinates[0]]

latitudes = []
longitudes = []
for x, y in zip(meta['Coordinates'],meta['Archive']):
	coords = make_coord(x,y)
	if coords is None:
		latitudes.append(None)
		longitudes.append(None)
		continue
	latitudes.append(coords[0])
	longitudes.append(coords[1])

meta['Latitude'] = latitudes
meta['Longitude'] = longitudes

del meta['Coordinates']


meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete_2.csv")
