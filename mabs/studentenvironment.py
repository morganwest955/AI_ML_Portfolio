# CS 440 Multi-Armed Bandit Assignment
# (C) 2017 Travis Mandel

#These imports should be sufficient
import random
import math
import distributions as dists
import environments as envs

#Write a comment explaining why UCB-1 must always be better than UCB-0.01, or
# a comment explaining your counterexample environment
class StudentEnv(envs.MABEnvironment):
    def __init__(self):
        #YOUR CODE HERE
        self.minReward = 0
        self.maxReward = 1
        self.numArms = 2
        self.alpha = [0.006,0.01]
        self.beta = [0.01,0.006]
        #pass #remove once implemented

    def pull(self,arm):
        #YOUR CODE HERE
        reward = self.dists[arm].sample()
        return (reward,[(arm,reward)])
        #pass #remove once implemented

    def reset(self):
        #YOUR CODE HERE
        self.dists = []
        for i in range(self.numArms):
            dist = dists.BetaDistribution(self.alpha[i],self.beta[i])
            self.dists.append(dist)
        return True #Change to return True once implemented
    
    def getNumArms(self):
        #YOUR CODE HERE
        return self.numArms
        #pass #remove once implemented
 
    def getMinReward(self):
        #YOUR CODE HERE
        return self.minReward
        #pass #remove once implemented
		
    def getMaxReward(self):
        #YOUR CODE HERE
        return self.maxReward
        #pass #remove once implemented
