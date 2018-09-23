# CS 440 Multi-Armed Bandit Assignment
# (C) 2017 Travis Mandel

from matplotlib import pyplot as plt
import learners
import environments as envs
import studentenvironment as studentenv


#Each graph is averaged over this many runs
NUM_ITERATIONS = 500


#(Learner, name) tuples
learnerTuples = [(learners.EpsilonGreedy(0.1), "Epsilon-Greedy-0.1"), (learners.UCB(1), "UCB-1"),\
                 (learners.UCB(0.01), "UCB-0.01"), (learners.ThompsonDiscrete(), "TS-Beta"),(learners.ThompsonContinuous(), "TS-Continuous")]
results = []
#(environment, name, tlimit) tuples)
#Temporarily removing all but one of these is a good way to test just one environment
#envTuples = [(envs.RandomizedGaussianEnv(10), "Gaussian10Arm", 300), (envs.RandomizedBinaryEnvironment(5,0), "Binary5Arm", 200), \
#            (envs.RandomizedBinaryEnvironment(5,30), "Delay5Arm", 300), (studentenv.StudentEnv(), "StudenEnv", 1000)]
envTuples = [(studentenv.StudentEnv(), "StudenEnv", 1000)]
for env,envName, tlimit in envTuples:
    trange = range(tlimit)
    envReady = env.reset()
    if not envReady:
        continue
    for learner,learnerName in learnerTuples:
        failed = False
        totalLearnerResults = [0.0] * len(trange) #init all-zero array
        for it in range(NUM_ITERATIONS):
            #set up the learner and the environment
            env.reset()
            inited = learner.initWithEnvironment(envs.MABEnvironmentInfo(env))
            if not inited:
                failed = True
                break
            
            cumReward = 0.0
            #Main loop, pulling arms, processing rewards, etc.
            for t in trange:
                chosen = learner.chooseArm()
                (reward, toProcess) = env.pull(chosen)
                cumReward += reward
                totalLearnerResults[t] += cumReward
                for (arm, reward) in toProcess:
                    learner.processReward(arm, reward)
        if failed: # due to unimplemented learner
            continue # With next learner

        #Average the results over the runs and plot
        avgResults = []
        for j in totalLearnerResults:
            avgResults.append(j/float(NUM_ITERATIONS))
        plt.plot(trange, avgResults, label=learnerName)

    #Format and write out the plot 
    plt.legend(loc='best')
    plt.xlabel("Timestep")
    plt.ylabel("Cumulative Reward")
    plt.savefig(envName + ".png")
    plt.clf()
    plt.cla()
    plt.close()
        
        

