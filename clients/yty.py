import networkx as nx
import altair as alt
import time,json
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy as npb
import Robogame as rg

def plot_scatter(type, df):
	scatter_plot = alt.Chart(df).mark_circle(color="black", opacity=0.1).transform_filter(
	    alt.FieldEqualPredicate(field='column', equal=f"{type}")
	).transform_filter(
	    alt.datum.winner != -2
	).encode(
	    x=alt.X("value:Q", title=f"{type}"),
	    y=alt.Y("Productivity:Q")
	)
	def fit_curve(df):
		if len(df) == 0:
			return 
		max_value = df['value'].max()
		min_value = df['value'].min()
		fit = np.polyfit(df['value'].astype(float), df['Productivity'].astype(float), 1)
		x = np.linspace(min_value,max_value,100)
		func = np.poly1d(fit)
		res = []

		for i in np.arange(0,len(x)):
			res.append({'column':df['column'], 'value':x[i], 'Productivity':func(x[i])})
		return res

	fit_df = df.loc[(df['column'] == type)&(df['winner'] != -2)]
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
    plot_type=['Repulsorlift Motor HP', 'Astrogation Buffer Length', 'Polarity Sinks', 'AutoTerrain Tread Count', 'InfoCore Size', 'Sonoreceptors', 'Cranial Uplink Bandwidth']

    plot_list = []
    for type in plot_type:
        plot_list.append(plot_scatter(type, part_df))

    return (plot_list[0] | plot_list[1]) & (plot_list[2] | plot_list[3]) & (plot_list[4] | plot_list[5]) & plot_list[6] 
