#!/usr/bin/env python

""" 
 Age Range [17, 82] and distributions in age as belowed:
   Age < 50: 74 persons
   50 <= Age < 60: 66 persons
   60 <= Age < 70: 84 persons
   Age >= 70: 49 persons
 
 So in training sets, cross-validation sets or test sets should
 follow the distributions. [1: 1: 1: 0.5] = [<60: 50-60: 60-70: >70]
"""

import os
import json
import random
import scipy.io as sio

FileA = "../cache/age_less_50"
FileB = "../cache/age_between_50_and_60"
FileC = "../cache/age_between_60_and_70"
FileD = "../cache/age_over_70"

DATA_DIR = '../data/PTB-mat'
CACHE_DIR = '../cache/ptb_train_cv_test_sets'

trainRatioA = 50
trainRatioB = 50
trainRatioC = 50
trainRatioD = 24

cvRatioA = 16
cvRatioB = 16
cvRatioC = 16
cvRatioD = 10

testRatioA = 8
testRatioB = 0 # always using ../cache/test_samples.part2
testRatioC = 18
testRatioD = 15

def getFirstColumnFromFile(filename):
    """ return a list represent the first column"""
    ret = []
    with open(filename) as f:
        for line in f.readlines():
            ret.append(line.split(' ')[0])
    # print ret
    # print len(ret)
    return ret

def loadMatFiles(dirname):
    content = []
    fullpath = DATA_DIR + '/' + dirname
    # print fullpath
    for filename in os.listdir(fullpath):
        name, ext = os.path.splitext(filename)
        if ext == '.mat':
            tmpData = sio.loadmat(fullpath + '/' + filename)['val']
            leadI = tmpData[0] # obtain leadI info; leadI is a ECG single
            # print leadI
            # print type(leadI)
            content.append(leadI.tolist())
    return content


def getSamples(setsType, partType, cols, ratio):
    if setsType == 'test' and partType == 'B' and ratio == 0:
        dirs = getFirstColumnFromFile('../cache/test_samples.part2')
    else:
        dirs = random.sample(cols, ratio)
    samples = {}
    for d in dirs:
        rawData = loadMatFiles(d)
        # print rawData
        samples[d] = rawData
    return samples

def getTrainSets(colA, colB, colC, colD):
    trainSets = {}
    partA = getSamples('train', 'A', colA, trainRatioA)
    partB = getSamples('train', 'B', colB, trainRatioB)
    partC = getSamples('train', 'C', colC, trainRatioC)
    partD = getSamples('train', 'D', colD, trainRatioD)

    trainSets.update(partA)
    trainSets.update(partB)
    trainSets.update(partC)
    trainSets.update(partD)

    return trainSets

def getCVSets(colA, colB, colC, colD):
    cvSets = {}
    partA = getSamples('cv', 'A', colA, cvRatioA)
    partB = getSamples('cv', 'B', colB, cvRatioB)
    partC = getSamples('cv', 'C', colC, cvRatioC)
    partD = getSamples('cv', 'D', colD, cvRatioD)

    cvSets.update(partA)
    cvSets.update(partB)
    cvSets.update(partC)
    cvSets.update(partD)

    return cvSets

def getTestSets(colA, colB, colC, colD):
    testSets = {}
    partA = getSamples('test', 'A', colA, testRatioA)
    partB = getSamples('test', 'B', colB, testRatioB)
    partC = getSamples('test', 'C', colC, testRatioC)
    partD = getSamples('test', 'D', colD, testRatioD)

    testSets.update(partA)
    testSets.update(partB)
    testSets.update(partC)
    testSets.update(partD)

    return testSets
    

def split():
    colA = getFirstColumnFromFile(FileA)
    colB = getFirstColumnFromFile(FileB)
    colC = getFirstColumnFromFile(FileC)
    colD = getFirstColumnFromFile(FileD)
    trainSets = getTrainSets(colA, colB, colC, colD)
    cvSets = getCVSets(colA, colB, colC, colD)
    testSets = getTestSets(colA, colB, colC, colD)
    
    return [trainSets, cvSets, testSets]

def setsDump(trainSets, cvSets, testSets):
    """
    Format
    {
        "patient001": [
            [1,2,3,...., 10000],
            [1,2,3,...., 10000]
        ],
        "patient002": [
            [1,2,3,...., 10000],
            [1,2,3,...., 10000]
        ],
        ...
        "patient100": [
            [1,2,3,...., 10000]
        ]
    }
    """
    with open(CACHE_DIR + '/train_sets', 'w') as f:
        json.dump(trainSets, f)
    with open(CACHE_DIR + '/cv_sets', 'w') as f:
        json.dump(cvSets, f)
    with open(CACHE_DIR + '/test_sets', 'w') as f:
        json.dump(testSets, f)


if __name__ == '__main__':
    [trainSets, cvSets, testSets] = split()
    setsDump(trainSets, cvSets, testSets)
