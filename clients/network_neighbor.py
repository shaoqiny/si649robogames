import streamlit as st
import time, json
import numpy as np
import altair as alt
import pandas as pd
import Robogame as rg
import networkx as nx
import nx_altair as nxa

game = rg.Robogame("bob")
data = game.getNetwork()
G = nx.node_link_graph(data)
robotInfo = game.getRobotInfo()

for n in G.nodes():
    G.nodes[n]['id'] =  n
    G.nodes[n]['weight'] =  G.degree[n]
    G.nodes[n]['winner'] = str(int(robotInfo[robotInfo['id']==n].winner))

# ### choose your interested node
pick_node = 1

if pick_node:
    neighbors = [n for n in G.neighbors(pick_node)] + [pick_node] 
    g = G.subgraph(neighbors)
else:
    g=G

pos = nx.spring_layout(g)

chart = nxa.draw_networkx(
    G=g,
    pos=pos,
    node_color='winner:N',    
    node_size='weight:Q',
    edge_color='lightgrey',
    node_tooltip=['id','weight','winner'],    
)

edges = chart.layer[0]
nodes = chart.layer[1]

# Build a brush
brush = alt.selection_interval(encodings=['x', 'y'])
color = alt.Color('winner:N',  legend=None)

# id_dropdown
options = list(nodes.data.id)
id_dropdown = alt.binding_select(options=options, name="id")
id_select = alt.selection_single(fields=['id'], bind=id_dropdown, name="id")

# Condition nodes based on brush
nodes = nodes.encode(
    fill=alt.condition(brush, color, alt.value('gray')),
).add_selection(
    brush,
    id_select
).transform_filter(
    id_select
)

# Create a bar graph to show highlighted nodes.
bars = alt.Chart(nodes.data).mark_bar().encode(
    x=alt.X('count()', scale=alt.Scale(domain=(0,100)), axis=alt.Axis(labels=False, title='Count of robots')),
    y='winner',
    color='winner',
).transform_filter(
    brush
).transform_filter(
    id_select
)

bars_text = bars.mark_text(align='left',dx=2).encode(
    text=alt.Text('count()', format='~s')
)

alt.vconcat(edges+nodes, bars+bars_text)




