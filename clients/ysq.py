import streamlit as st
import time, json
import numpy as np
import altair as alt
import pandas as pd
import Robogame as rg
import networkx as nx
import nx_altair as nxa

#新增关于productivity和time的dataframe
def generate_df(robots, cur_time):
    data_list = []  #这个不要放在循环里
    item1 = {'team': "team 1", 'time': cur_time, 'productivity': robots[robots.winner == 1]['Productivity'].sum()}
    item2 = {'team': "team 2", 'time': cur_time, 'productivity': robots[robots.winner == 2]['Productivity'].sum()}
    data_list.append(item1)
    data_list.append(item2)
    return pd.DataFrame(data_list)

def plot_productivity_time(robots, cur_time):
    df = generate_df(robots, cur_time)
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['time'], empty='none')
    line = alt.Chart(df).mark_line(interpolate='basis').encode(
        x='time:Q',
        y='productivity:Q',
        color='id:N'
    )

    selectors = alt.Chart(df).mark_point().encode(
        x='time:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'productivity:Q', alt.value(' '))
    )

    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='time:Q',
    ).transform_filter(
        nearest
    )

    return alt.layer(line, selectors, points, rules, text)

def plot_winner(robots):
    team_1_productivity = robots[robots.winner == 1]['Productivity'].sum()
    team_2_productivity = robots[robots.winner == 2]['Productivity'].sum()
    data_source = pd.DataFrame({"team": ['team1', 'team2'], "productivity": [team_1_productivity, team_2_productivity]})
    base = alt.Chart(data_source).properties()
    bar = base.mark_bar().encode(
        x= alt.X('sum(productivity)',scale=alt.Scale(domain=[0, team_1_productivity+team_2_productivity])),
        color='team',
        tooltip = ['team', 'productivity']
    )
    # pie = base.mark_area().encode(
    #     theta=alt.Theta(field="productivity", type="quantitative"),
    #     color=alt.Color(field="team", type="nominal"),
    #     tooltip = ['team', 'productivity']
    # )
    rule = base.mark_rule(color='black').encode(
        x='median(productivity)',
        size=alt.value(3)
    )
    return (bar + rule)

def productivity_winner(robots, cur_time):
    return alt.vconcat(plot_productivity_time(robots, cur_time), plot_winner(robots))
