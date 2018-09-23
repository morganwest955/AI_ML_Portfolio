"""
CS 440 Hidden Markov Model Assignment

Travis Mandel, modified from
an assignment by Sravana Reddy
"""

import string
import math

# The HMM Model
#
# In this HMM, states and observations are represented by strings (usually single characters)
#
# Transitions are stored as a nested map from starting state
#  and ending state to probability. So to get the
# probability of going from state i to state j, 
# should do self.transitions[i][j]
#
# The initial probabilities are stored in the same data structure,
# but the starting state is set to a special value '#'
# So self.transitions['#'][j] representes the probability of being
# in state j initially.
#
# Emissions are stored as a nested map from starting state
#  and emission to probability. So to get the
# probability of getting emission e in state i, one
# should do self.emissions[i][e]
#
# NOTE: Emissions/Transitions that are missing from the maps are assumed to
# have probability 0.
#
# You can get the states with self.states, but be careful as this does not
# include the start state #.
class HMM:

    def __init__(self, transitions=None, emissions=None):
        self.transitions = transitions
        self.emissions = emissions
        if self.emissions:
            self.states = self.emissions.keys() #note: self.states excludes the start state
            

    # Read HMM from files
    # It reads separate files for the emissions (basename.emit) and for the
    # transitions (basename.trans)
    # Files are read line-by-line, with a separate transition or emission
    # probability on each line
    def load(self, basename):
        
        transf = open(basename+ ".trans", "r")
        self.transitions = {}
        self.emissions = {}
        for line in transf:
            tokens = string.split(line, " ")
            fromstate = tokens[0]
            tostate = tokens[1]
            prob = float(tokens[2])
            if fromstate not in self.transitions:
                self.transitions[fromstate] = {}
            self.transitions[fromstate][tostate] = prob
        transf.close()
            
        emitf = open(basename+ ".emit", "r")
        for line in emitf:
            tokens = string.split(line, " ")
            state = tokens[0]
            obs = tokens[1]
            prob = float(tokens[2])
            if state not in self.emissions:
                self.emissions[state] = {}
            self.emissions[state][obs] = prob
        emitf.close()
        self.states = self.emissions.keys()
            
        
    # Write HMM to file
    # It writes out two files: one for the emissions (basename.emit) and
    # the other for the transitions (basename.trans)
    # Files are written line-by-line, with a separate transition or emission
    # probability on each line
    def dump(self, basename):
        transf = open(basename+ ".trans", "w+")
        for fromstate in self.transitions:
            for tostate in self.transitions[fromstate]:
                prob = self.transitions[fromstate][tostate]
                if prob > 0:
                    transf.write(fromstate + " " + tostate + " " + str(prob) + "\n")
        transf.close()

        emitf = open(basename+ ".emit", "w+")
        for state in self.emissions:
            for obs in self.emissions[state]:
                prob = self.emissions[state][obs]
                if prob > 0:
                    emitf.write(state + " " + obs + " " + str(prob) + "\n")
        emitf.close()

        
    # method that checks if the given state and observation combination are in emissions
    # if not, return 0.  Else, return the emission.
    def emissionsCheck(self, state, o):
        if state not in self.emissions or o not in self.emissions[state]:
            return 0
        return self.emissions[state][o]
                    
    # Belief at the given time of state X is equal to the probablility of state X given the evidence so far at the time
    # Given an observation, runs the forward algorithm
    # This should return the unnormalized forward beliefs,
    # aka alpha_i(t), in the form beliefs[t][i]
    def forward(self, observation):
        obs = observation.asList()
        forward = [{}]        
        for state in self.states: # initialize every value to zero
            forward[0][state] = self.transitions['#'][state] * self.emissionsCheck(state, obs[0])
        for o in xrange(1,len(obs)):
            forward.append({}) # empty dict entry to fill out later
            v = [] # just a list to save stuff for doing arithmetic later
            for state1 in self.states:
                for state2 in self.states: # iterate through states
                    # arithmetic for forward algorithm
                    v.append(float(self.transitions[state2][state1] * forward[o-1][state2]))
                s = math.fsum(v) * self.emissionsCheck(state1,obs[o])
                forward[o][state1] = s
                v = [] # reset list after appending
        return forward


    #Computes the overall probability of the output sequence
    # using the forward algorithm.
    # This function is correct, do not change!
    def forward_probability(self, observation):
        t = len(observation)-1
        res = self.forward(observation)
        if res is None:
            return -1
        return sum(res[t].values())

    #Runs the viterbi algorithm on an observation
    # and returns a list of hidden states
    # indicating the most likely sequence given the model
    def viterbi(self, observation):        
        obs = observation.asList()
        viterbi = [{}]
        back = [{}]
        for state in self.states:
            viterbi[0][state] = self.transitions['#'][state] * self.emissionsCheck(state,obs[0])
            back[0][state] = None
        for o in xrange(1,len(obs)):
            viterbi.append({})
            back.append({})
            for state1 in self.states:
                maxVal = 0
                maxState = None
                for state2 in self.states:                   
                    val = float(self.transitions[state2][state1] * viterbi[o-1][state2] * \
                                   self.emissionsCheck(state1,obs[o]))
                    if val > maxVal:
                        maxVal = val
                        maxState = state2
                viterbi[o][state1] = maxVal
                back[o][state1] = maxState
        
        # iterate through each word and pick the state with the max probablility for each one
        maxVal = 0
        maxState = None
        for state in self.states:        
            if viterbi[len(obs)-1][state] > maxVal:
                maxVal = viterbi[len(obs)-1][state]
                maxState = state
        currentState = maxState
        hiddenStates = []
        for t in range(len(obs)-1,-1,-1):
            hiddenStates.append(currentState)
            currentState = back[t][currentState]    
        #print hiddenStates
        hiddenStates.reverse()
        return hiddenStates
                
        pass #remove once implemented



    # Given an observation, runs the backward algorithm
    # This should return the unnormalized backwards beliefs,
    # aka beta_i(t), in the form beliefs[t][i]
    def backward(self, observation):
        obs = observation.asList()
        # YOUR CODE HERE
        end = len(obs)
        obs = observation.asList()
        backward = [{}]        
        for state in self.states: # initialize every value to zero
            backward[0][state] = 1
        for o in xrange(end-1,0,-1):
            backward.insert(0,{}) # empty dict entry to fill out later          
            for state1 in self.states:
                v = [] # just a list to save stuff for doing arithmetic later
                for state2 in self.states: # iterate through states
                    # arithmetic for forward algorithm
                    v.append(float(self.transitions[state1][state2] * backward[1][state2] * \
                                                                    self.emissionsCheck(state2,obs[o])))
                s = math.fsum(v)
                backward[0][state1] = s
                v = [] # reset list after appending
        return backward
        pass #remove once implemented


    #Computes the overall probability of the output sequence
    # using the backward algorithm.
    # This function is correct, do not change!
    def backward_probability(self, observation):

        #Got to push backwards prob on time 0 back to initial state
        res = self.backward(observation)
        if res is None:
            return -1
        obs = observation.asList()
        finalRes = 0
        for s in res[0]:
            finalRes += res[0][s]* \
                self.transitions['#'][s]*self.emissions[s].get(obs[0],0)
        return finalRes

    #Is this HMM equal to another HMM, with some tolerance?
    def isEqual(self, other, tolerance):
        for i in self.transitions:
            if i not in other.transitions:
                print "Extra transition: " + str(i) 
                return False
            for j in self.transitions[i]:
                if abs(self.transitions[i][j] - other.transitions[i].get(j,0)) > tolerance:
                    print "Transitions differ! " +i +" " + j +" "+ str(self.transitions[i][j]) + " " +str( other.transitions[i].get(j,0))
                    return False
        for i in self.emissions:
            if i not in other.emissions:
                print "Extra emission: " + str(i) 
                return False
            for e in self.emissions[i]:
                if abs(self.emissions[i][e] - other.emissions[i].get(e,0)) > tolerance:
                    print "Emissions differ! " +i +" " + e +" "+ str(self.emissions[i][e]) + " " +str( other.emissions[i].get(e,0))
                    return False

        return True
        



    # Runs the EM aka Baum Welch aka Forward-Backward algorithm
    # to learn the parameters of the HMM without any supervision.
    #
    # The data comes in a corpus, where each element of the corpus
    # is a sequence of type Observation.  Consider doing observation.asList()
    # to make these sequences easier to work with.
    #
    # The algorithm should stop when the log-likelihood changes by less than
    # 'convergence'.  It's probabaly a good idea to print out the log-likelihood
    # on each iteration so you can see what is going on.
    #
    # Should return the final log-likelihood of the entire corpus.
    #
    # Note: DO NOT initialize the parameters randomly, they should already be
    #    initialized to something when this method is called.
    def learn_unsupervised(self, corpus, convergence=0.069):
        # YOUR CODE HERE
        pass #remove once implemented
       
        
                
            

 
