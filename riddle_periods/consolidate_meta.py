# consolidate metadata with riddle content
import pandas as pd
import os


def df(location):
	meta = pd.read_csv(location, encoding='utf-8')
	return meta


def create_gale():
	gale = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/gale/"
	meta = "/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/gale_metadata.csv"
	
	# _THE_RIDDLE_THAT_MAD_DX1901124530
	# "THE RIDDLE THAT MADE COUNT BISMARCK SICK" // GALE|DX1901124530
	
	# A_DOUBLE_Missionary__CC1903068950
	# A DOUBLE Missionary Enigma // GALE|DX1901124530

	# A_LITTLE_GAME_DX1901052543
	# A LITTLE GAME // GALE|DX1901052543

	meta_df = df(meta)


	files = [file for file in os.listdir(gale) if not file.startswith('.')]

	txt_files = {}

	for file in files:
		with open(gale+file) as f:
			txt = f.read()
		txt_files[file.split('.txt')[0]] = txt

	for key,value in txt_files.items():
		clean_key = key[-12:]
		if clean_key[:2] not in ['DX','CC']:
			clean_key = key[-15:]

		index = meta_df.index[clean_key==meta_df.id].tolist()
		meta_df.at[index, 'content']=value
		if meta_df.loc[index, 'content'].empty:
			print(index)
			# print(meta_df.loc[[index]])
			# print("Generated: " + str(clean_key))
			# print("Actual:    " + str(meta_df.loc[index,'id']))


	meta_df.to_csv('/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/full_df.csv')


create_gale()




