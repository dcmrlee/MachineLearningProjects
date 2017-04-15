#!/usr/bin/env python

"""
Load train-sets, cv-sets, test-sets
"""

import os
import traceback
import numpy as np

from log import logger

def _readSetsFile(filename):
    arr = np.array([])
    try:
        arr = np.load(filename)
        #with open(filename) as f:
        #    for line in f:
        #        arr.append(line.strip().split(' '))
    except Exception as e:
        logger.warn(str(e))
        traceStr = traceback.format_exc()
        logger.warn(traceStr)
    
    logger.info('finish loading ' + filename)
    return arr

def load_train_cv_test(dirname):
    trainSetsFile = os.path.join(dirname, 'trainSets.npy')
    cvSetsFile = os.path.join(dirname, 'cvSets.npy')
    testSetsFile = os.path.join(dirname, 'testSets.npy')

    trainSets = _readSetsFile(trainSetsFile)
    cvSets = _readSetsFile(cvSetsFile)
    testSets = _readSetsFile(testSetsFile)

    """
    print len(trainSets)
    print len(cvSets)
    print len(testSets)
    """
    
    return [trainSets, cvSets, testSets]
