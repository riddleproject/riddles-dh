import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
from os import listdir
from datetime import datetime


file = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/complete csvs/BoF Dataframe_Nov4.csv"

df = pd.read_csv(file).reset_index(drop=True)


df.rename(columns = {'Location':'Library'}, inplace = True) 
df.rename(columns = {'Place Published':'Location'}, inplace = True)
df.rename(columns = {'Date':'Date2'}, inplace = True) 

def guess_date(string):
    for fmt in ["%B %d, %Y", '%B, %Y', "%B %Y", '%Y-%m-%d', '%d-%b-%y', '%m/%d/%y', '%Y']:
        try:
            date = datetime.strptime(string, fmt)
            if date.year >= 2000:
            	date -= pd.DateOffset(years=100)
            return date.strftime("%B %d, %Y")
        except ValueError:
            continue
    return np.nan

dates = [str(date) for date in df['Event_Date'].tolist()]
dates = [guess_date(date) for date in dates]
print(dates)
df['Date'] = dates
print(df['Date'])


df['Archive'] = 'Enigmatic Bill of Fare'

def get_loc(place, n):
    if place is np.nan:
    	return None
    if n == 0:
        return None
    try:
        location = geolocator.geocode(place)
        if location is None:
            return None

        coord = [location.longitude, location.latitude] 
        return coord
    except:
        return get_loc(place, n-1)

print("Getting coordinates.")
geolocator = Nominatim(user_agent='doodad')
df['Coordinates'] = df.apply((lambda row:get_loc(row['Location'],10)), axis=1)
print('Done coordinates.')

df.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/complete csvs/BoFs.csv")

old = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/Complete_Menus_Oct29.csv")
new = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/complete csvs/BoFs.csv")
let = pd.concat([old, new], sort=False).reset_index()
let = let.dropna(subset=['Archive'])
let = let.loc[:,"'File' Attachments":]

let.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/Complete_Menus.csv")
