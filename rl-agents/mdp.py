# CS 440 Reinforcement Learning Assignment
# (C) 2017 Travis Mandel

#These imports should be sufficient
import random
import distributions as dists
import sys

#Object representing a fully-defined
# Makov Decision Process (MDP)
class MDP:
    #obsProbs must be a map from (s,a) --> list of outcome probabilities
    def  __init__(self, env, obsProbs):
        # Do not change this
        self.env = env
        self.obsProbs = obsProbs
        if not self.validate():
            sys.exit(-1)
		
    def validate(self):
        # Do not change this
        for pair in self.obsProbs:
            probs = self.obsProbs[pair]
            if abs(1-sum(probs)) > 0.0001:
                print "Trying to construct invalid mdp! (s,a)= " + \
                      str(pair) + " oProbs " + str(probs)
                return False
            
        return True

    def vectorSum(self,vector):
        vecSum = 0
        for num in vector:
            vecSum = vecSum + num
        return vecSum
    # Recursively run through the finite horizon algorithm      
    def V(self, state,t,p):

        #given the state, find an action that hasn't been put in the dict yet and run the recursive algorithm for it
        if t >= 0: # if the time horizon hasn't been reached
            # continue iterating through recursive step
            # have to get action and outcome of state+action before running recursive step
            # not really sure the actual correct way to get the next action sooo

            #In order to use the reward as a scalar for the outcome vector, I somehow need to get outcome into an int.
            #If I sum all of the outcomes in a vector together, it equals 1 every time
            #So it doesn't throw an error if I do that, but it's not the right answer.
            for a in range(0,self.env.getNumActions()): # iterate through all actions in the 
                if self.env.isActionValid(state,a): # if the action is valid
                    outcome = self.obsProbs[(state,a)]
                    print "outcome",outcome
                    action = a
            policy = self.vectorSum(outcome)*self.env.getReward(state,action,self.vectorSum(outcome))
            self.V(self.env.getNextState(state,action,self.vectorSum(outcome)),t-1,p+policy) # recursive step
        else:
            policy = p
            
            return (state,t)
    # Should return a dict mapping (s,t) --> a
    # Where a is the optimal long-term action to take in this MDP
    def computeOptimalPolicy(self):
        #YOUR CODE HERE
        vList = {}
        print self.env.getTimeHorizon()
        initState = self.env.getInitialState()
        print initState                
        pickState = self.V(initState,self.env.getTimeHorizon()-1,0)
        print "pickState",pickState
        return pickState

    #Generates an outcome sampled according to the MDP.
    def sampleOutcome(self, state, action):
        # Do not change this
        if not self.env.isActionValid(state, action):
            print "Error: Trying to take invalid action. " + \
                  "At state " + str(state) + " taking action " + str(action)
            sys.exit(-1)
        probs = self.obsProbs[(state,action)]
        choice = random.random()
        sumP = 0
        for i in range(len(probs)):
            sumP += probs[i]
            if choice < sumP:
                return i

        print "Error! Should have sampled a value by now!"
        sys.exit(-1)
            
                    
                
