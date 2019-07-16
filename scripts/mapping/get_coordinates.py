# gets the latitude and longitude of the locations of the suppers and attaches it to the existing dataframe

import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from geopy.exc import GeocoderTimedOut
from progress.bar import Bar


def get_loc(place):
    try:
        location = geolocator.geocode(place)
        try:
            coord = (location.latitude, location.longitude)
        except:
            coord = None
    except GeocoderTimedOut:
        return(get_loc(place))
    return coord


meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/master_locations.csv")

meta = meta.loc[:,'Newspaper':'Aditional_Comments']

meta = meta.dropna(how='all')

countries = meta['Country']
states = meta['State/Province']
cities = meta['City']

coords = []
geolocator = Nominatim(user_agent='ndrezn')

bar = Bar('Processing...', max=len(cities))
for city,state,country in zip(cities,states,countries):
    try:
        place = str(city)+ " " +str(state)+ " " + str(country)
        coord = get_loc(place)   
        coords.append(coord)
    except GeocoderTimedOut:
        sleep(30)
        geolocator = Nominatim(user_agent='ndrezn')
        coord = get_loc(place)
        coords.append(coord)

bar.finish()

print("Coordinates collected.")
print(broken)
meta['Coordinates'] = coords
meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/with_coordinates.csv")