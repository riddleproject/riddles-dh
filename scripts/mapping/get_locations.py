from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
from os import listdir


path = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/broken_up/"
paths = [f for f in listdir(path) if not f.startswith(".")]

dfs = [pd.read_csv(path+f).reset_index(drop=True) for f in paths]

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

dfs_new = []
for df in dfs:
    geolocator = Nominatim(user_agent='doodad')
    df['Coordinates'] = df.apply((lambda row:get_loc(row['Location'],10)), axis=1)
    dfs_new.append(df)


meta = pd.concat(dfs, sort=False)

meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete_w_coord.csv")

