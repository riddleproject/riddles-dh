# Generate graph from CSV

import pandas as pd
from igraph import *

meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/networks/BOF_Unique_Riddles_numbers_Final.csv")
meta = meta.loc[:, 'UN':'BOF_Appearance_Number']
meta = meta.dropna(subset=['BOFs containing riddle'])
meta['BOFs containing riddle'] = meta.apply(lambda row: (row['BOFs containing riddle']).split(';'), axis=1)

g = Graph()
bofs = list(set([item for sublist in meta['BOFs containing riddle'] for item in sublist]))
g.add_vertices(len(bofs))
g.vs['name'] = bofs


def build_edges(cur, edgelist, line):
	for node in edgelist:	
		eid = g.get_eid(node,cur, error=False)
		if eid >= 0:
			g.es[eid]['weight'] += 1
			g.es[eid]['Label'].append(line)
			print(g.es[eid['Label']])
		else:
			g.add_edge(cur, node, weight=1, Label=[line])
	if len(edgelist) > 1:
		build_edges(edgelist.pop(), edgelist, line)
	else:
		return 1

for edgelist, line in zip(meta['BOFs containing riddle'], meta['Riddle']):	
	build_edges(edgelist.pop(), edgelist, line)

print(g)
g.write_graphml("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/networks/BOFs_as_network.GraphML")
