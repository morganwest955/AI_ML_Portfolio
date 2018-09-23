# CS 440 Multi-Armed Bandit Assignment
# (C) 2017 Travis Mandel

import numpy


    
# Simple class for a Normal (Gaussian) Distribution
#
# Parameters: mean (mu) and standard deviation (sigma)
class NormalDistribution(object):
    def __init__(self, mean, stdDev):
        self.mean = mean
        self.stdDev = stdDev

    #Draws a single sample from the distribution
    def sample(self):
        samples = numpy.random.normal(self.mean, self.stdDev, 1)
        return samples[0]

    #gets the standard deviation
    def getStdDev(self):
       return self.stdDev


    #gets the mean
    def getMean(self):
       return self.mean


# Simple class for a Normal (Gaussian) Distribution
#   which is truncated to some given range
#
# Parameters: mean (mu), standard deviation (sigma), minVal, maxVal
class TruncatedNormalDistribution(object):
    def __init__(self, mean, stdDev, minVal, maxVal):
        self.mean = mean
        self.stdDev = stdDev
        self.minVal = minVal
        self.maxVal = maxVal

    #Draws a single sample from the distribution
    def sample(self):
        samples = numpy.random.normal(self.mean, self.stdDev, 1)
        sample = samples[0]
        if sample < self.minVal:
            return self.minVal
        if sample > self.maxVal:
            return self.maxVal
        return sample

    #gets the base standard deviation (may not be actual due to truncation)
    def getStdDev(self):
       return self.stdDev


    #gets the base mean (may not be actual due to truncation)
    def getMean(self):
       return self.mean

# Simple class for a Beta Distribution
# Parameters: alpha and beta
class BetaDistribution(object):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    #Draws a single sample from the distribution
    def sample(self):
        samples = numpy.random.beta(self.alpha, self.beta, 1)
        return samples[0]

    #get alpha parameter
    def getAlpha(self):
       return self.alpha


    #gets beta parameter
    def getBeta(self):
       return self.beta

    
        
