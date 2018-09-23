# CS 440 Reinforcement Learning Assignment
# (C) 2017 Travis Mandel

import distributions as dists
import sys


#Basic empirical check of Dirichlet mean and variance
testdist = [2,4,1]
ansM = [0.2882184309811832, 0.5734013658563103, 0.1383802031625066]
ansV = [0.02553761724210567, 0.02926463420790286, 0.01583368158909755]

dist = dists.DirichletDistribution(testdist)
total = [0,0,0]
NUM_ITERATIONS = 1000
for i in range(NUM_ITERATIONS):
    probs = dist.sample()
    for j in range(len(probs)):
        total[j] += probs[j]/NUM_ITERATIONS

totalV = [0,0,0]
for i in range(NUM_ITERATIONS):
    probs = dist.sample()
    for j in range(len(probs)):
        totalV[j] += ((probs[j]-total[j])*(probs[j]-total[j]))/NUM_ITERATIONS

scoreM = sum([abs(total[i]-ansM[i]) for i in range(len(total))]) 
if scoreM > 0.05:
    print "Fail: Total values: " + str(total) + " off by " + str(scoreM)
    sys.exit(-1)

scoreV = sum([abs(totalV[i]-ansV[i]) for i in range(len(totalV))]) 
if scoreV > 0.008:
    print "Fail: TotalV values: " + str(totalV) + " off by " + str(scoreV)
    sys.exit(-1)

print "Tests passed!"


        
        

