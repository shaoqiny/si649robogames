import streamlit as st
import time, json
import numpy as np
import altair as alt
import pandas as pd
import Robogame as rg
import networkx as nx
import nx_altair as nxa


def get_family(cur_node, tree):
    aGraph = nx.tree_graph(tree)
    family = [cur_node]
    predecessors = list(aGraph.predecessors(cur_node))
    family.extend(predecessors)
    successors = list(aGraph.successors(cur_node))
    family.extend(successors)
    # return family
    for p_node in predecessors:
        siblings = list(aGraph.successors(p_node))
        for s_node in siblings:
            if s_node != cur_node:
                family.append(s_node)
    # relate_list = siblings + parent
    return family

def vis_network_dry(rid, tree, network, robots):
	# global rid
	# rid = user_input
	print("robot id = ", rid)
	tree_graph = nx.tree_graph(tree)
	linked_graph = nx.node_link_graph(network)

	for n in linked_graph.nodes():
		linked_graph.nodes[n]['weight'] = linked_graph.degree[n]
		linked_graph.nodes[n]['id'] = n
		linked_graph.nodes[n]['owner'] = int(robots[robots['id']==n].winner)

	neighbors = [n for n in linked_graph.neighbors(rid)]
	neighbors.append(rid)
	socialnetwork = linked_graph.subgraph(neighbors)
	socialnetwork_chart = nxa.draw_networkx(
	    socialnetwork,
	    node_color='owner:N',
		cmap='accent',
		edge_color='#d7dcde',
	    node_size = 'weight',
	    node_tooltip = ['id','owner','weight'],
	).properties(width=200, height=200)

	# family network
	family = get_family(rid, tree)
	family.append(rid)
	familynetwork = tree_graph.subgraph(family)

	for n in tree_graph.nodes():
		tree_graph.nodes[n]['id'] = n
		tree_graph.nodes[n]['owner'] = int(robots[robots['id']==n].winner)

	family_chart = nxa.draw_networkx(
		familynetwork,
		node_color='owner:N',
		cmap='accent',
		edge_color='#d7dcde',
		node_tooltip = ['id','owner'],
	)
		
	return family_chart
