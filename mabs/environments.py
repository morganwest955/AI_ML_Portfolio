# CS 440 Multi-Armed Bandit Assignment
# (C) 2017 Travis Mandel

import random
import distributions as dists

#Interface provided to the learner for getting the known aspects of the environment
#Takes in a fully defined environment and "hides" unknown info
class MABEnvironmentInfo:
    def  __init__(self, env):
        self.numArms = env.getNumArms()
        self.minReward = env.getMinReward()
        self.maxReward = env.getMaxReward()
		
    def getNumArms(self):
        return self.numArms
		
    def getMinReward(self):
        return self.minReward
		
    def getMaxReward(self):
        return self.maxReward
    

#A fully-defined Multi-Armed Bandit Environment
class MABEnvironment:
    def pull(self,arm):
        pass

    #Re-initializes the environment from scratch
    #Returns True if reset successful, False otherwise
    def reset(self):
        pass

    def getNumArms(self):
        return self.NumArms
		
    def getMinReward(self):
        pass

    def getMaxReward(self):
        pass

class RandomizedGaussianEnv(MABEnvironment):
    def __init__(self, numArms):
        #hardcoded values to reduce variance
        self.numArms = numArms
        
        self.means = [0.1, 0.13, 0.8, 0.9, 0.3, 0.2, 0.69, 0.1, 0.0, 0.1]

        self.stddevs = [0.8,0.9,1.0, 0.8, 0.9, 1.0, 0.8, 0.9, 1.0, 0.8]
        #initializae everything
        self.reset()
        

    def pull(self,arm):
        reward = self.dists[arm].sample()
        return (reward, [(arm, reward)])

    def reset(self):
        #generate a randomized range of min and max rewards
        self.maxReward = 75
        self.minReward = -25
        self.dists = []
        for i in range(self.numArms):
            dist = dists.TruncatedNormalDistribution(self.means[i]*100-25,
                                            self.stddevs[i]*100,
                                            self.minReward,
                                            self.maxReward)
            self.dists.append(dist)
        return True

    def getNumArms(self):
        return self.numArms
		
    def getMinReward(self):
        return self.minReward
		
    def getMaxReward(self):
        return self.maxReward

#A Binary environment, with possible delay in the form of batches
class RandomizedBinaryEnvironment(MABEnvironment):
    def __init__(self, numArms, delay):
        self.maxReward = 1
        self.minReward = -1
        
        self.numArms = numArms
        self.delay = delay
       

    def pull(self,arm):
        reward = None
        if random.random() < self.dists[arm]:
            reward = self.maxReward
        else:
            reward = self.minReward

        self.lastBatch.append((arm, reward))
        returnedFback = []
        if(len(self.lastBatch) > self.delay):
                returnedFback = self.lastBatch
                self.lastBatch = []

        return (reward, returnedFback)

    def reset(self):
        self.dists = [0.1,0.2,0.0, 0.1, 0.9, 0.8, 0.0,0.0,0.1, 0.2]
        self.lastBatch = []
        return True
    
    def getNumArms(self):
        return self.numArms
 
    def getMinReward(self):
        return self.minReward
		
    def getMaxReward(self):
        return self.maxReward


        
    
    
