"""
CS 440 Hidden Markov Model Assignment

Travis Mandel, modified from
an assignment by Sravana Reddy
"""

import random
import argparse
import codecs
import os
import sys
import hmm
import observations



def compareFiles(student, ref, ignoreOrder=False):
    sfile = open(student, "r")
    rfile = open(ref, "r")
    if ignoreOrder:
        slines = set()
        rlines = set()
        for sline in sfile:
            slines.add (sline)
            
        for rline in rfile:
            rlines.add(rline)
        if len(slines) != len(rlines):
            print "Different number of lines! student has " + str(len(slines))\
                    + " but ref has " + str(len(rlines))
            return False
        for sline in slines:
            if sline not in rlines:
                print "Incorrect student line: " + str(sline)
                return False
        sfile.close()
        rfile.close()
        return True
            
    slines = []
    rlines = []
    for sline in sfile:
        slines.append (sline)
        
    for rline in rfile:
        rlines.append(rline)
    if len(slines) != len(rlines):
        print "Different number of lines! student has " + str(len(slines))\
                + " but ref has " + str(len(rlines))
        return False
    for i in range(len(slines)):
        if slines[i] != rlines[i]:
            print "Incorrect student line: " + str(slines[i]) + " should be " + str(rlines[i])
            return False
    sfile.close()
    rfile.close()
    return True

# main
def main():

    model = hmm.HMM()



    print "-------------Preliminary setup----------------"
    if True:
        existingFile = 'models/two_english'
        newFile = "two_english_test"
        model.load(existingFile)
        model.dump(newFile)
        eq = compareFiles(newFile + ".emit", existingFile+".emit", True)
        if eq:
            eq2 = compareFiles(newFile + ".trans", existingFile+".trans", True)
        if eq and eq2:
            print "HMM read/write works correctly"
        else:
            print "HMM read/write failed!"
            sys.exit(-1)

    print "-------------Forward Algorithm----------------"
    if True:
        model.load("models/partofspeech.browntags.trained")
        obsfilebase = "data/ambiguous_sents"
        corpus = observations.load_observations(obsfilebase+".obs")
        outputfile = obsfilebase+'.forwardprob'
        o2 = []
        with open(outputfile, 'w') as o:
            for observation in corpus:
                res = model.forward(observation)
                if res is not None:
                    o2.append(res[2]['VERB'])
                o.write(str(model.forward_probability(observation))+'\n')

        refo2 = [0.0, 0.0, 0.0, 3.653679756807993e-11, 0.0, 0.0, 4.312565970191802e-12, 3.654779278846958e-11, 1.6086166116798018e-07, 0.0, 0.0]
        for i in range(len(refo2)):
            if len(o2) <= i:
                print "Error: Nothing returned from Forward Algorithm!"
            elif abs(o2[i] -refo2[i]) > 1e-14:
                print "Error in Forward Algorithm: Probability of Verb at t=2 should be " + str(refo2[i]) + " not " + str(o2[i])


        eq = compareFiles(outputfile, "gold/ambiguous_sents.prob")
        if eq:
            print "Forward Algorithm passed basic sanity check"
        else:
            print "Error in Overall Forward Probability"

    print "-------------Viterbi Algorithm----------------"
    if True:
        model.load("models/partofspeech.browntags.trained")
        obsfilebase = "data/ambiguous_sents"
        corpus = observations.load_observations(obsfilebase+".obs")
        outputfile = obsfilebase+'.tagged.obs'

        with codecs.open(outputfile, 'w', 'utf8') as o:
            for observation in corpus:
                stateseq = model.viterbi(observation)
                if stateseq is None:
                    continue
                observation.stateseq = stateseq  # adds most likely states as
                                                 # 'tags' on observation
                o.write(str(observation))

        eq = compareFiles(outputfile, "gold/ambiguous_sents.tagged.obs")
        if eq:
            print "Viterbi Completed Successfully"
        else:
            print "Error in Viterbi"
        


    print "-------------Backwards Algorithm----------------"
    if True:
        model.load("models/partofspeech.browntags.trained")
        obsfilebase = "data/ambiguous_sents"
        corpus = observations.load_observations(obsfilebase+".obs")
        outputfile = obsfilebase+'.backwardprob'
        o2 = []
        with open(outputfile, 'w') as o:
            for observation in corpus:
                res = model.backward(observation)
                if res is not None:
                    o2.append(res[2]['VERB'])
                o.write(str(model.backward_probability(observation))+'\n')

        refo2 = [2.3589871535491068e-07, 1.8514313765823803e-13, 2.140512612882977e-06, 2.0333825508441356e-06, 4.339252852607301e-10, 1.4033802247403003e-09, 1.4162117145319527e-08, 5.011761202650785e-06, 2.0776974177243364e-09, 5.391970636677047e-07, 2.147210857790581e-07]
        for i in range(len(refo2)):
            if len(o2) <= i:
                print "Error: Nothing returned from Backward Algorithm!"
            elif abs(o2[i] -refo2[i]) > 1e-14:
                print "Error in Backward Algorithm: Probability of Verb at t=2 should be " + str(refo2[i]) + " not " + str(o2[i])

        eq = compareFiles(outputfile, "gold/ambiguous_sents.prob")
        if eq:
            print "Backward Algorithm passed basic sanity check"
        else:
            print "Error in Overall Backward Probability"

    print "------------------EM--------------------"
    if True:
        modelbase = "models/two_english"
        model.load(modelbase)
        obsfilename = "english_words"
        obsfilebase = "data/" + obsfilename
        corpus = observations.load_observations(obsfilebase+".obs")
        log_likelihood = model.learn_unsupervised(corpus)
        #write the trained model
        ref_likelihood =  -105954.94191 # -152860.669251 in base 2
        if log_likelihood is None or abs(log_likelihood - ref_likelihood) > 0.05:
            print "Error: likelihood should be " + str(ref_likelihood) + \
                  " but is " + str(log_likelihood)
        finalprefix = modelbase+'.'+obsfilename+'.trained'
        model.dump(finalprefix)
        goldprefix = "gold/two_english.english_words.trained"


        learnedModel = hmm.HMM()
        learnedModel.load(finalprefix)

        refModel = hmm.HMM()
        refModel.load(goldprefix)
        
        eq = learnedModel.isEqual(refModel, 1e-13)
        if eq:
            print "EM implemented correctly!"
        else:
            print "Error in EM"

if __name__=='__main__':
    main()
