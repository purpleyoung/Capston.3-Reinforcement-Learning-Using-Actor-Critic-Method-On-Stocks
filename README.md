The goal of this project is to implement and evaluate the performance of the actor-critic method (A2C). The evaluation will use the Anytrade, a 3rd party OpenAI ML gym enviornment, which provides an action space of buy, hold, and sell as well as some scoring functionality. For visual representation of the model's performance I use quantstats, which takes in the a backtest environement and returns a robust trading profile from which specific charts or statistics can be called.

[GitHub](http://github.com)

http://www.github.com/
https://stable-baselines.readthedocs.io/en/master/index.html

Reinforcement learning thrives on massive amounts of data and for any practcal use requires the discovery and implementation of algorithms capable of efficiently developing action policies within processing and even data constraints. In the case of A2C, the model's architecture provides for steep optimizations in computing efficiency, and optimal policy discovery. In fact, unlike other exlporations of cumputational optimization like using GPUs or in the case of A3C using multiple environmnets, A2C uses multiple instances of the same learning agent in a single enviornment, each progressing through the same series of states and relaying what they've learned to the policy netowrk which will only periodically update all agents with the average of weighted learning.

To briefly illustrate this process say there were multiple instances of youself, and each one experienced the same series of events throughout the same day; some making rewarding choices and ohers making not-so-rewarding choices. And at the end of that day, these agents would gather and sharing their knowledge and experiences, with each gaining the average insight of the whole, even though they themselves didn't make the decisions that led to this update in their understanding. Over series of days, an optimal policy for navigating the day emerges.

This is the concept behind actor critic.

In some forms of A2C The learning process takes place between two deep neural networks, the first approximates the agents policy since it's simply probability distriution over a set of actions where we take the state as input and output a probability for each action. The latter is the critic wwhich approximates the value function, determining whether or not the resulting state is of value. So, the actor selects action, critic evaluates the resultant state's expected value - informing the actor via reward, and the result is compared the the environment. This creates a feedback, as the actor improves, so does the critic in it's ability to correctly evaluate the actor.


### The Data
Using the AlphaVantage API I called for stock, volume, and some commonly used technical indicators used for technical analysis of statistical features relevant to a stocks price action and behavior. Seeking to perhaps mimic in some way an innovative feature of A3C, A2C's asynchronous predecessor which ultized multiple enviornments, I developed the netowrk repeatedly, on 63 tech sector stocks taken from the same time periods (3 training, 1 validation, and 1 test splits) through a battery of similar but slightly different environemtns, each using a pandaas dataframe of the alphavantage data after it's been munged and set to the correct datetime range.

### The Method: A2C
Over the course of this project, partcularly in the discovery phase, I encounted a wide swath of libraries offering environments and implementations for a variety of algorithms. Some libraries offer a limited array both of agents and environenments while others support highly specialized and inclusive model-enviornment ecosystems. Taking all this into account, I decided to source the implemtation of A2C from the aptly named StandardBaselines library which standard. Through this I gained some valuable insight into the terrain of reinforcement learning as an area of research and plan to explore the libraries and limits further.

### Visualizing Training

For this I used tensorboard which allowed for easy analysis of the model's learning rates and patterns. Unfortunately, tensorboard did not give full labelling for its outpiut graphs.
Y here would be the average amount of reward at that learning update and X is steps taken.
Each line represents the daily reward gained by buying, holding, selling one each stock during this training split (image from split 1). As each of the 63 stocks was fed into the enviornemnt the critic and actor-value netowrks gradually, for the most part, improved their ability to cause actions leading to the accumulation of reward. 

Now, fed a training seperate set of both unseen data and an unseen market period the reward trendlines perform much better.

Speaking of trends, I didn't have to detrend my data since we're maximizing reward and also because, through our model, we aren't trying to replicate a denoised pattern - we're learning to navigate highly dynamic data!


Here we have a table providing for visual analysis on a monthly and yearly basis. I'd like to enrich the data I train on my including features outside of stock market that could explain and improve this behavior.
