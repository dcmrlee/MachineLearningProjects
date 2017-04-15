#!/usr/bin/env python

"""
    Total 290 persons 
      50% of them considered as known
      the other 50% of them as unknown

    Each '*.mat' data file has 10000 dimensions (10000 numbers)
    Every 1000 numbers represented 1 seconds
    So each one '*.mat' file represented 10 seconds
"""

import os
import json
import random
import traceback
import scipy.io as sio
import numpy as np

from log import logger

DATA_DIR = '../data/PTB-mat'
CACHE_DIR = '../cache/ptb_train_cv_test_sets'

def getTotalPersons(dataDir):
    """ return person list 
    Example:
        ['patient001', 'patient002', ...]
    """
    personList = []
    try: 
        for subdir in os.listdir(dataDir):
            if os.path.isdir(os.path.join(dataDir, subdir)):
                if 'patient' in subdir:
                    personList.append(subdir)
    except Exception as e:
        logger.warn(str(e))
        traceStr = traceback.format_exc()
        logger.warn(traceStr)
        
    return personList

def randomDepartPersons(personList):
    """
    return two list
        - known person list (50%)
        - unknown person list (50%)
    """
    listLen = len(personList)
    tmpList = random.sample(personList, listLen)
    half = int(listLen/2) + 1
    knownPersons = tmpList[:half]
    unknownPersons = tmpList[half:]

    return [knownPersons, unknownPersons]

def readMatFiles(dirList):
    """
    Format of variable samples
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
    samples = {}
    for subdir in dirList:
        dirPath = os.path.join(DATA_DIR, subdir)
        arr = []
        try:
            for name in os.listdir(dirPath):
                prefix, ext = os.path.splitext(name)
                if ext == '.mat':
                    filename = os.path.join(dirPath, name)
                    matData = sio.loadmat(filename)
                    leadI = matData['val'][0].tolist() # obtain leadI info; leadI is a ECG single
                    arr.append(leadI)
        except Exception as e:
            logger.warn(str(e) + subdir)
            traceStr = traceback.format_exc()
            logger.warn(traceStr)

        samples[subdir] = arr

    return samples

def cutSampleBySecond(vals, sec):
    """
    vals is a list, like:
        [[1,2,3,...,10000],[1-10000], [1-10000],...]
        every 1000 val is one second, every 10000 val is 10 seconds
    sec is a number, if it is 2, meaning divide 10 by 2

    The result return by this function is (sec is 2 for example)
        [[1-2000], [1-2000], [1-2000], ...]
    """
    result = []
    base = 1000
    step = base * sec
    count = 0
    for val in vals:
        tmp = [val[i:i+step] for i in range(0, len(val), step)]
        count += len(tmp)
        result += tmp
    return result

def addLabel(samples, label):
    for sample in samples:
        sample.append(label)

def sampleSplit(samples, knownPersons, unknownPersons):
    trainSets = []
    cvSets = []
    testSets = []
    trainRatio = 0.6
    cvRatio = 0.2
    testRatio = 0.2
    for person, vals in samples.items():
        smallSamples = cutSampleBySecond(vals, 2)
        length = len(smallSamples)
        # random order
        randomSamples = random.sample(smallSamples, length)

        if person in knownPersons:
            label = 1
        elif person in unknownPersons:
            label = 0
        else:
            logger.warn('not found person number' + person)
            continue

        addLabel(randomSamples, label)

        trainLen = int(trainRatio * length)
        cvLen = int(cvRatio * length)
        testLen = int(testRatio * length)
        
        trainSets += randomSamples[0:trainLen]
        cvSets += randomSamples[trainLen:trainLen+cvLen]
        testSets += randomSamples[trainLen+cvLen:]
        
    return [trainSets, cvSets, testSets]

def dumpSets(lists, filename):
    filepath = os.path.join(CACHE_DIR, filename)
    try:
        np.save(filepath, np.array(lists))
        # with open(filepath, 'w') as f:
            #for l in lists:
            #    for n in l:
            #        f.write(str(n) + ' ')
            #    f.write('\n')
    except Exception as e:
        logger.warn(str(e) + ' filename')


if __name__ == '__main__':
    personList = getTotalPersons(DATA_DIR)
    [knownPersons, unknownPersons] = randomDepartPersons(personList)
    # print knownPersons
    # print unknownPersons
    # print len(knownPersons)
    # print len(unknownPersons)
    samples = readMatFiles(personList)
    [trainSets, cvSets, testSets] = sampleSplit(samples, knownPersons, unknownPersons)
    dumpSets(trainSets, 'trainSets')
    dumpSets(cvSets, 'cvSets')
    dumpSets(testSets, 'testSets')
