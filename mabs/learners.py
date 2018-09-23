# CS 440 Multi-Armed Bandit Assignment
# (C) 2017 Travis Mandel

#These imports should be sufficient
import random
import math
import environments as envs
import distributions as dists

# Interface (abstract) for multiarmed bandit learners
# Don't change this
class MABLearner(object):

    # Re-initilializes the MAB with a given MABEnvironment
    # Returns True if initialization was successful, False otherwise
    def initWithEnvironment(self,env):
        pass

    #Chooses an arm to pull based on all the rewards processed so far
    # Arms are represented as integers, so it just needs to return a
    # number between 0 and the number of arms in the environment
    def chooseArm(self):
        pass

    #Processes a reward
    def processReward(self, arm, reward):
        pass


# Implements the epsilon-greedy algorithm as discussed in class
# Note: To break ties, just pick the arm with lower index
#(probably the way you would naturally implement it anyway)
# Note 2: The greedy phase selects the highest arm out of
# those that have been pulled
class EpsilonGreedy(MABLearner):

    def __init__(self, epsilon):
        #YOUR CODE HERE
        self.epsilon = epsilon
        self.arms = None
        self.values = None
        self.counts = None
        
        #pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        self.minReward = env.getMinReward()
        self.maxReward = env.getMaxReward()
        self.arms = env.getNumArms()
        self.counts = [0 for c in range(self.arms)]
        self.values = [0 for c in range(self.arms)]
        return True #Change to return True once implemented

    def chooseArm(self):
        #YOUR CODE HERE
        if random.random() > self.epsilon:
            return self.values.index(max(self.values))
        else:
            return random.randint(0,self.arms -1)
        
        #pass #remove once implemented

    def processReward(self,arm, reward):
        #YOUR CODE HERE
        self.counts[arm] = self.counts[arm] + 1
        newValue = ((self.counts[arm]-1)/float(self.counts[arm]))*self.values[arm]+(1/float(self.counts[arm]))*reward
        self.values[arm] = newValue
        #pass #remove once implemented

# Implements the UCB algorithm as discussed in class
# Note: To break ties, just pick the arm with lower index
#(probably the way you would naturally implement it anyway)
class UCB(MABLearner):
    #Pull each arm until a reward is recieved
    #when the arm receives a reward, calculate the UCB and save
    #Locate the max UCB value for all arms and keep pulling that arm
    def __init__(self, alpha):
        #YOUR CODE HERE
        self.alpha = alpha
        self.arms = 0
        self.values = 0
        self.counts = 0
        #pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        self.arms = env.getNumArms()
        self.environment = env
        self.counts = [0 for c in range(self.arms)]
        self.values = [0 for c in range(self.arms)]
        self.hasReward = [False for c in range(self.arms)]
        self.allArmsGotReward = False
        self.UCBValue = [0 for c in range(self.arms)]
        self.upperBound = 0
        self.numRewards = [0 for c in range(self.arms)]
        self.hasReward = [False for c in range(self.arms)]
        self.sumOfRewards = [0 for c in range(self.arms)]
        return True #Change to return True once implemented

    def pickMaxUpperBound(self):
        maxUpperBound = 0
        maxUpperBoundIndex = 0
        for i in range(0,self.arms):
            if self.UCBValue[i] > maxUpperBound:
                maxUpperBound = self.UCBValue[i]
                maxUpperBoundIndex = i
        return maxUpperBoundIndex
    
    def chooseArm(self):
        #YOUR CODE HERE

        #pull all of the arms
        if not self.allArmsGotReward:
            for i in range(0,self.arms):
                if not self.hasReward[i]: #if arm has not recieved reward, pull it
                    return i
        
        #UCB algorithm
        #u_i + sqrt(2log(t)/numArmPulls[i])
        for i in range(0,self.arms):
            u_i = self.sumOfRewards[i]/float(self.counts[i]) #imperical mean of rewards seen so far
            t = 0 #sum of all numArmPulls
            totalRewards = 0
            for j in range(0,self.arms):
                t = t + self.counts[j]
            upperBound = u_i + (self.alpha * math.sqrt((2 * math.log(t))/float(self.counts[i])))
            self.UCBValue[i] = upperBound
        
        #check if all arms got reward
        self.allArmsGotReward = True
        for i in range(0,self.arms):
            if not self.hasReward[i]:
                self.allArmsGotReward = False
                
        return self.pickMaxUpperBound()

        
        
        #pass #remove once implemented
        
    def processReward(self,arm, reward):
        #YOUR CODE HERE
        #print "processing arm ",arm
        self.hasReward[arm] = True
        self.counts[arm] = self.counts[arm] + 1
        minReward = self.environment.getMinReward()
        maxReward = self.environment.getMaxReward()
        scaleFactor = maxReward - minReward
        newValue = (reward - minReward) / float(scaleFactor)
        self.values[arm] = newValue
        self.sumOfRewards[arm] = self.sumOfRewards[arm] + self.values[arm]
        #pass #remove once implemented

# Implements the Beta-Bernoulli thompson sampling algorithm as discussed
#in class.
#Prior should be a Beta(1,1)
#Should handle the straightforward extension to non-discrete variables.
class ThompsonDiscrete(MABLearner):
#following psuedocode from agrawal13.pdf
    def __init__(self):
        self.arms = None
        self.values = None
        self.counts = None
        self.alpha = []
        self.beta = []
        #self.betaDistribution = distributions.BetaDistribution
        #pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        #self.bD = dists.BetaDistribution()
        self.arms = env.getNumArms()
        self.values = [0 for c in range(0,self.arms)]
        self.counts = [0 for c in range(0,self.arms)]
        self.minReward = env.getMinReward()
        self.maxReward = env.getMaxReward()
        self.alpha = [1 for c in range(0,self.arms)]
        self.beta = [1 for c in range(0,self.arms)]
        return True #Change to return True once implemented

    def pickMaxSample(self):
        maxSample = 0
        maxSampleIndex = 0
        for i in range(0,self.arms):
            betaDist = dists.BetaDistribution(self.alpha[i],self.beta[i])
            sample = betaDist.sample()
            if sample > maxSample:
                maxSample = sample
                maxSampleIndex = i
        return maxSampleIndex
    
    def chooseArm(self):
        #YOUR CODE HERE
        return self.pickMaxSample()                
        
        #pass #remove once implemented
        
    def processReward(self,arm, reward):
        #YOUR CODE HERE
        scaleFactor = self.maxReward - self.minReward
        newValue = (reward - self.minReward) / float(scaleFactor)

        if random.random() > newValue:
            self.beta[arm] = self.beta[arm] + 1
        else:
            self.alpha[arm] = self.alpha[arm] + 1
        
        #pass #remove once implemented

# Implements the Normal-Normal thompson sampling algorithm designed for
# continuous distributions
class ThompsonContinuous(MABLearner):

    def __init__(self):
        self.arms = None
        self.values = None
        self.counts = None
        self.mean = []
        self.stddev = []
        #pass #remove once implemented
        
    def initWithEnvironment(self,env):
        #YOUR CODE HERE
        self.arms = env.getNumArms()
        self.values = [0 for c in range(0,self.arms)]
        self.counts = [0 for c in range(0,self.arms)]
        self.minReward = env.getMinReward()
        self.maxReward = env.getMaxReward()
        self.mean = [1 for c in range(0,self.arms)]
        self.stddev = [1 for c in range(0,self.arms)]
        self.sumOfRewards = [0 for c in range(self.arms)]
        self.listOfRewards = []
        return True #Change to return True once implemented

    def pickMaxSample(self):
        maxSample = 0
        maxSampleIndex = 0
        for i in range(0,self.arms):
            normDist = dists.NormalDistribution(self.mean[i],self.stddev[i])
            sample = normDist.sample()
            if sample > maxSample:
                maxSample = sample
                maxSampleIndex = i
        return maxSampleIndex
    
    def chooseArm(self):
        #YOUR CODE HERE
        return self.pickMaxSample()                
        
        #pass #remove once implemented
        
    def processReward(self,arm, reward):
        #YOUR CODE HERE
        self.counts[arm] = self.counts[arm] + 1
        scaleFactor = self.maxReward - self.minReward
        newValue = (reward - self.minReward) / float(scaleFactor)
        temp = (arm, newValue)
        self.listOfRewards.append(temp)
        self.sumOfRewards[arm] = self.sumOfRewards[arm] + newValue
        
        self.mean[arm] = self.sumOfRewards[arm] / float(self.counts[arm])
        valueMinusMeanSquared = []
        for listArm, listReward in self.listOfRewards:
            if listArm == arm:
                vmm = listReward - self.mean[arm]
                valueMinusMeanSquared.append(vmm*vmm)
        sumOfVmm = 0
        if self.counts[arm] > 1:
            for i in range(0,len(valueMinusMeanSquared)-1):
                sumOfVmm = sumOfVmm + valueMinusMeanSquared[i]
            self.stddev[arm] = math.sqrt(sumOfVmm/float(self.counts[arm]-1))
        else:
            self.stddev[arm] = 1
        
        
        
        """
        self.mean[arm] = self.sumOfRewards[arm]/(self.counts[arm]+1)
        self.stddev[arm] = math.sqrt(1/(self.counts[arm]+1))
        """
        #pass #remove once implemented



        

