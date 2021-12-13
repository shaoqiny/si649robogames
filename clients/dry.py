import streamlit as st
import time, json
import numpy as np
import altair as alt
import pandas as pd
import Robogame as rg
import networkx as nx
import nx_altair as nxa

# # let's create two "spots" in the streamlit view for our charts
# user_input = int(st.number_input("label goes here", 0))

# status = st.empty()
# predVis = st.empty()
# partVis = st.empty()
# treeVis = st.empty()

def get_family(cur_node, tree):
	familyGraph = nx.tree_graph(tree)
	family = [cur_node]

	predecessors = list(familyGraph.predecessors(cur_node))
	family.extend(predecessors)
	successors = list(familyGraph.successors(cur_node))
	family.extend(successors)
	
	for p_node in predecessors:
		siblings = list(familyGraph.successors(p_node))
		for s_node in siblings:
			if s_node != cur_node:
				family.append(s_node)

	return family


def vis_network_dry(rid, tree, robots):
	tree_graph = nx.tree_graph(tree)

	for idx in tree_graph.nodes():
		tree_graph.nodes[idx]['robot_id'] = idx
		tree_graph.nodes[idx]['robot_owner'] = int(robots[robots['id'] == idx].winner)

	# family network
	family = get_family(rid, tree)
	familynetwork = tree_graph.subgraph(family)

	family_chart = nxa.draw_networkx(
		familynetwork,
		cmap='viridis',
		node_color='robot_owner:N',
		edge_color='black',
		node_tooltip = ['robot_id','robot_owner'],
	).properties(width=500,height=300)

	return family_chart

# #def main():
# # create the game, and mark it as ready
# game = rg.Robogame("bob")
# game.setReady()

# for i in np.arange(0,101):

# 	# update the hints
# 	game.getHints()

# 	# # create a dataframe for the time prediction hints
# 	# df1 = pd.DataFrame(game.getAllPredictionHints())
# 	# # get the parts
# 	# df2 = pd.DataFrame(game.getAllPartHints())

# 	tree = game.getTree()
# 	network = game.getNetwork()
# 	robots = game.getRobotInfo()
# 	# print(robots)
# 	# exit()

# 	# # if it's not empty, let's get going
# 	# if (len(df1) > 0):
# 	# 	# create a plot for the time predictions (ignore which robot it came from)
# 	# 	c1 = alt.Chart(df1).mark_circle().encode(
# 	# 		alt.X('time:Q',scale=alt.Scale(domain=(0, 100))),
# 	# 		alt.Y('value:Q',scale=alt.Scale(domain=(0, 100)))
# 	# 	)

# 	# 	# write it to the screen
# 	# 	predVis.write(c1)

# 	# # we'll want only the quantitative parts for this
# 	# # the nominal parts should go in another plot
# 	# quantProps = ['Astrogation Buffer Length','InfoCore Size',
# 	# 	'AutoTerrain Tread Count','Polarity Sinks',
# 	# 	'Cranial Uplink Bandwidth','Repulsorlift Motor HP',
# 	# 	'Sonoreceptors']

# 	# # if it's not empty, let's get going
# 	# if (len(df2) > 0):
# 	# 	df2 = df2[df2['column'].isin(quantProps)]
# 	# 	c2 = alt.Chart(df2).mark_circle().encode(
# 	# 		alt.X('column:N'),
# 	# 		alt.Y('value:Q',scale=alt.Scale(domain=(-100, 100)))
# 	# 	)
# 	# 	partVis.write(c2)
# 	tree_graph = nx.tree_graph(tree)
# 	# print(tree_graph.nodes[0])
# 	# exit()
# 	vis_network()

# 	# sleep 6 seconds
# 	for t in np.arange(0,6):
# 		status.write("Seconds to next hack: " + str(6-t))
# 		time.sleep(1)
	
# # if __name__ == "__main__":
# # 	predVis = st.empty()
# # 	partVis = st.empty()
# # 	treeVis = st.empty()
# # 	main()
