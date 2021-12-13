import streamlit as st
import time
import numpy as np
import Robogame as rg

import dry, zx, ysq, yty


st.set_page_config(layout='wide')

# create the game, and mark it as ready
game = rg.Robogame("bob")
game.setReady()

# GUI starts here

# Title
st.header('SI 649 Robogame Dashboard')

status = st.empty()

# Main Plots, update every six seconds
col1, col2 = st.beta_columns((1,1.4))

with col1:
    input_1 = st.number_input('Enter node interested in', 0)
    st.subheader('Current Robot Social Network')
    c1_vis_network_1 = st.empty()
    st.subheader('Current Robot Family Tree')
    c1_vis_network_2 = st.empty() 

with col2:
    st.subheader('Sum of Productivity for each Team')
    c2_productivity_winner = st.empty()
    st.subheader('Relationship between Productivity and Parts')
    c2_scatter = st.empty()

test = st.empty()

# initialize

# Time
curtime = st.empty()

# wait for both players to be ready
while(True):	
	gametime = game.getGameTime()
	timetogo = gametime['gamestarttime_secs'] - gametime['servertime_secs']
	
	if ('Error' in gametime):
		status.write("Error"+str(gametime))
		break
	if (timetogo <= 0):
		status.write("Let's go!")
		break
	status.write("waiting to launch... game will start in " + str(int(timetogo)))
	time.sleep(1) # sleep 1 second at a time, wait for the game to start

data_list = list()

# run 100 times
for i in np.arange(0,101):
	# sleep 6 seconds

    for t in np.arange(0,6):
        status.write("Seconds to next hack: " + str(6-t))
        time.sleep(1)
    
    game.getHints()

    # get data from game object
    game_time = game.getGameTime()['curtime']
    game_tree = game.getTree()
    game_network = game.getNetwork()
    game_robots = game.getRobotInfo()
    game_parthints = game.getAllPartHints()


    c1_vis_network_1.write(zx.vis_network_zx(int(input_1), game_network, game_robots))

    c1_vis_network_2.write(dry.vis_network_dry(int(input_1), game_tree, game_robots))

    c2_productivity_winner.write(ysq.productivity_winner(game_robots, game_time, data_list))

    c2_scatter.write(yty.scatter_charts(game_robots, game_parthints))
