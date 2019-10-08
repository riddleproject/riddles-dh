# split coordinates from original CSV into two columns and add them to the CSV

import pandas as pd
import numpy as np

meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete.csv")
meta=meta.dropna(axis=1,how='all')


def make_coord(coord, archive):
	if coord is np.nan or coord is None:
		return None,None
	coordinates = (coord[:-1])[1:].split(',')
	coordinates = [float(coord) for coord in coordinates]
	if (coordinates[0] > -10):
		if archive != 'British Newspaper Archives':
			return None,None
	if (coordinates[1] < 15):
		return None,None
	return (coordinates[1], coordinates[0])

meta['Latitude'], meta['Longitude'] = zip(*meta.apply(lambda row: make_coord(row['Coordinates'],row['Archive']), axis=1).tolist())

del meta['Coordinates']


meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete_2.csv")
