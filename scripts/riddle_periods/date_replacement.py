# replace dates in the unformatted metadata sheet with datetime objects

import pandas as pd
import datetime

# load up the sheet of data
train = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mod_df.csv")

def guess_date(string):
    for fmt in ["%B %d, %Y", "%B %Y"]:
        try:
            return datetime.datetime.strptime(string, fmt)
        except ValueError:
            continue
    return None

old_dates = [str(date) for date in train['DATE'].tolist()]

dates = [guess_date(date) for date in old_dates]

train['DATE'] = dates

train = train.reset_index()


train.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mod_df2.csv")