# Script to reformat endnote data as a CSV

import pandas as pd

# enter the file input:
text_in = "ENTER_INPUT_HERE.txt"
csv_out = "ENTER_OUTPUT_HERE.csv"

#####################################
# DO NOT CHANGE ANYTHING BELOW HERE #
#####################################

# load up the sheet of data
txt = open(text_in, 'r')

# read in the text file
txt = txt.read()

# split the text into the different items
items = txt.split('\n\n')

# list to contain each row for the dataframe
rows_list = []

# iterate through each item (i.e. row)
for cur in items:
	# dict to contain the row data
	cur_dict = {}
	# split the item by line (i.e. column)
	cur = cur.split('\n')
	# iterate through each data point (column)
	for item in cur:
		# split each column into its (column title, column data) pair
		line = item.split(': ')
		# make sure split output correctly, i.e. there's actually data there
		if len(line) < 2:
			continue
		# update dict with the new (column, data) pair
		cur_dict[line[0]]=line[1]
	# add new dict as a row
	rows_list.append(cur_dict)

# generate dataframe from rows
df = pd.DataFrame(rows_list)       
# save dataframe
df.to_csv(csv_out)