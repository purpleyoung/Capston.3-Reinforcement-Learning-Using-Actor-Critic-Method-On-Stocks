import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime


import pandas_datareader.data as web


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins

# from src.data_pipeline import preprocess_data

# Gym
import gym
import gym_anytrading

# Stable baselines 1.15
#TODO look at adding the rest if/as needed
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C, SAC, ACER, PPO2, TD3
# from stable_baselines import DDPG, GAIL

# tf 
import tensorflow as tf

# core
import numpy as np
import pandas as pd
import quantstats as qs

from mpld3 import plugins

# image_directory = './'
# list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
# static_image_route = '/static/'


# Init
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.title = "ML Sock Predict"

# Layout
app.layout = html.Div(children=[
    html.H1('Stock Visualization Dashboard'),
    html.H4('Please enter the stock name'),
    dcc.Input(id="input", value='', type='text'),
    # add input for date range
    html.Div(id="output-graph")
])


# User Inputs
@app.callback(
    Output(component_id="output-graph", component_property='children'),
    [Input(component_id="input", component_property="value")]
)

def update_value(input_data):
    # model = A2C.load("a2c_cartpole")
    # df = preprocessing(ticker=input_data)
    # env = gym.make('stocks-v0', df=df, frame_bound=(90,110), window_size=5)

    # while True: 
    # obs = env.reset()
    #     action, _states = model.predict(obs)
    #     obs = obs[np.newaxis, ...]
    #     if done:
    #     obs, rewards, done, info = env.step(action)    
    #         break
    #         #print("info", info)
    # plt.figure(figsize=(16, 6))
    # qs.extend_pandas()
    # plt.savefig('hope.png')
    # env.render_all()

    # net_worth = pd.Series(env.history['total_profit'], index=df.index[start_index+1:end_index])
    # returns = net_worth.pct_change().iloc[1:]
    # html.Img()
    return 5

    
    # return dcc.Graph(id="demo", figure={'data': [z], 'layout': {'title': input_data}})

    #return dcc.Graph(id="demo", figure=mpld3.show())

########### Run the app
if __name__ == '__main__':
    application.run(debug=True, port=5000)