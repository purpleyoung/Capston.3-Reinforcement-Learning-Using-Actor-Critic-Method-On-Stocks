# core
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Gym
import gym
import gym_anytrading
import base64

# Stable baselines 1.15
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C, SAC, ACER, PPO2, TD3
# from stable_baselines import DDPG, GAIL

# tf
#TODO add tensorflow-gpu ability
import tensorflow as tf

# data visualization
import quantstats as qs

# allows preprocessing function to be called where/as necessary.
from src.data_pipeline import preprocess_data


### EDA: A Random Walk
# Initialize env
# df = pd.read_csv('data/30day-AAPL.csv')
# env = gym.make('stocks-v0', df=df, frame_bound=(5,200), window_size=5)
# state = env.reset()
# while True: 
#    action = env.action_space.sample()
#    n_state, reward, done, info = env.step(action)
#    if done: 
#        print("info", info)
#        break
        
#plt.figure(figsize=(15,6))
#plt.cla()
#env.render_all()
#plt.show()

### Descriptives
# env.signal_features
# env.action_space
# state = env.reset()

### Environment
def env_func():
    """[Builds environment and wraps it in a dummy vector.]

    Returns:
        [env]: [Training environment]
    """
    df = preprocess_data(ticker,period)
    env_maker = lambda: gym.make('stocks-v0', df=df, frame_bound=(5,100), window_size=5)
    env = DummyVecEnv([env_maker])
    return env

### Model
def A2C_():
    """[Builds, trains, saves, and returns an A2C model]

    Returns:
        [model]: [Actor Critic Model]
    """
    env = env_func()
    policy_kwargs = dict(net_arch=[64, 'lstm', dict(vf=[128, 128, 128], pi=[64, 64])])
    model = A2C('MlpLstmPolicy', env, verbose=0) 
    # train
    model.learn(total_timesteps=50000)
    # save
    model.save("a2c_cartpole")
    return model




### Backtesting
def backtest(ticker,period): 
    """[Backtests the model against unseen data]

    Args:
        ticker ([string]): [ticker indicating which stoc to test against]
        period ([string]): [indicates date range for backtest]

    Returns:
        [env]: [env object with test result values]
    """
    model = A2C.load("a2c_cartpole")
    df = preprocess_data(ticker,period)
    env = gym.make('stocks-v0', df=df, frame_bound=(10,50), window_size=5)
    obs = env.reset()
    while True: 
        obs = obs[np.newaxis, ...]
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        if done:
            print("info", info)
            break
    return env