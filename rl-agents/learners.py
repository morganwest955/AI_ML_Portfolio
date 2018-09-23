# CS 440 Reinforcement Learning Assignment
# (C) 2017 Travis Mandel

#These imports should be sufficient
import random
import math
import environments as envs
import distributions as dists
import mdp

# Interface (abstract) for reinforcement learning agents
# Don't change this
class RLAgent(object):

    # Re-initializes the agent with a given RLEnvironment
    # Returns True if initialization was successful, False otherwise
    def initWithEnvironment(self,env):
        pass

    #Chooses a a valid action based on all the feedback processed so far
    # Actions are represented as integers, so it just needs to return a
    # number between 0 and the number of actions in the environment
    def chooseAction(self, state, t):
        pass

    #Processes an episode, which is a list of (state, action, outcome) tuples.
    def processEpisode(self, episode):
        pass
	
    #Signals to the agent that a new episode is about to start
    def episodeStart(self):
	pass


# Implements the PSRL Algorithm as discussed in class
# Implement the version with alpha_i=1 (uniform)
class PSRL(RLAgent):

    def __init__(self):
        #YOUR CODE HERE
        pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        return False #Change to return True once implemented
                
    def chooseAction(self, state, t):
        #YOUR CODE HERE
        pass #remove once implemented

    def episodeStart(self):
        #YOUR CODE HERE
        pass #remove once implemented
        
    def processEpisode(self, episode):
        #YOUR CODE HERE
        pass #remove once implemented
			

# Implements the basic Q-Learning algorithm as discussed in class
class QLearner(RLAgent):
#Q(s,a,t)<-(1-a)Q(s,a,t)+a[R(s,a,o)+maxQ(T(s,a,o),a',t+1)]
    def __init__(self, epsilon, alpha):
        #YOUR CODE HERE
        Q = (0,0,0)
        R = (0,0,0)
        T = (0,0,0)
        pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        return False #Change to return True once implemented

    def chooseAction(self, state, t):
        #YOUR CODE HERE
        pass #remove once implemented
            
    def episodeStart(self):
        #YOUR CODE HERE
        pass #remove once implemented
		
    def processEpisode(self, episode):
        #YOUR CODE HERE
        pass #remove once implemented




