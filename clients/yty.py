import networkx as nx
import altair as alt
import time,json
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy as npb
import Robogame as rg

def plot_scatter(df,type):
	scatter_plot = alt.Chart(df).mark_circle(color="black", opacity=0.2).transform_filter(
	    alt.datum.winner != -2
	).encode(
	    x=alt.X("value:Q", title=type),
	    y=alt.Y("Productivity:Q")
	)

	def fit_curve(df):
		if len(df)==0:
			return []
		if (df['value'].isnull().any() and df['Productivity'].isnull().any()): return []
		print('fit',df)
		max_value = df['value'].max()
		min_value = df['value'].min()
		## judge whether value is float
		fit = np.polyfit(df['value'].astype(str).astype(float), df['Productivity'].astype(str).astype(float), 1)
		x = np.linspace(min_value,max_value,100)
		func = np.poly1d(fit)
		res = []
				
		for i in np.arange(0,len(x)):
			res.append({'column':df['column'], 'value':x[i], 'Productivity':func(x[i])})
		return res

	fit_df=df[df.winner!=-2]
	res = fit_curve(fit_df)
	
	fit_plot = alt.Chart(alt.Data(values=res)).mark_line().encode(
		x='value:Q',
		y='Productivity:Q'
	)

	return (scatter_plot + fit_plot).properties(
	    height=150,
	    width=100
	)

def scatter_charts(robots, hints):
	parthints_df = pd.read_json(json.dumps(hints), orient='records')
	if len(parthints_df) == 0:
		return
	part_df = pd.merge(parthints_df, robots, how='left', on='id')
	plot_type_q=[ 'Polarity Sinks', 'AutoTerrain Tread Count',  'Sonoreceptors', 'Cranial Uplink Bandwidth','Repulsorlift Motor HP', 'Astrogation Buffer Length','InfoCore Size']
	plot_list = []
	for type in plot_type_q:
		type_df=part_df[part_df.column==type]
		plot_list.append(plot_scatter(type_df,type))

	plot_type_n=[ 'Axial Piston Model','Nanochip Model','Arakyd Vocabulator Model']

	for type in plot_type_n:
		type_df=part_df[part_df.column==type]
		plot_list.append(plot_bar(type_df,type))   
	

	return (plot_list[0] | plot_list[1] | plot_list[2] | plot_list[3] |plot_list[4]) & ( plot_list[5] | plot_list[6] | plot_list[7] | plot_list[8] | plot_list[9]) 


def plot_bar(df,type):
	scatter = alt.Chart(df).mark_circle(opacity=0.4,color='black').transform_filter(
	    alt.datum.winner!=-2
	).encode(
	    x=alt.X("value:N",title=type),
	    y=alt.Y("Productivity:Q")
	)
	
	bar = alt.Chart(df).mark_bar(opacity=0.3).transform_filter(
	    alt.datum.winner!=-2
	).encode(
	    x=alt.X("value:N"),
	    y=alt.Y("mean(Productivity):Q"),
	    tooltip=['value:N','mean(Productivity)']
	)
	return scatter+bar