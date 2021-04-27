import numpy as np
import pandas as pd
from gym.utils import seeding
import gym
from gym import spaces




HMAX_NORMALIZE = 100 install
INIT_ACCOUNT_BALANCE=100000
STOCK_DIM = 30
FEE_PERCENT = 0.003
REWARD_SCALING = 1e-4

class trainEnv(gym.Env):
    # metadata = {'render.modes': ['human']}
    def __init__(self, df,day = 0):
        self.day = day
        self.df = df
        self.action_space = spaces.Box(low = -1, high = 1,shape = (STOCK_DIM,)) 
        self.observation_space = spaces.Box(low=0, high=np.inf, shape = (181,))
        self.data = self.df.loc[self.day,:]
        self.terminal = False             
        self.state = [INIT_ACCOUNT_BALANCE] + \
                      self.data.adjcp.values.tolist() + \
                      [0]*STOCK_DIM + \
                      self.data.macd.values.tolist() + \
                      self.data.rsi.values.tolist() + \
                      self.data.cci.values.tolist() + \
        self.reward = 0
        self.cost = 0
        self.asset_memory = [INIT_ACCOUNT_BALANCE]
        self.rewards_memory = []
        self.trades = 0
        self._seed()