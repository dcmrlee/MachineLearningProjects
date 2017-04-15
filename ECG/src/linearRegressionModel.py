#!/usr/bin/evn python

"""
Using Linear Regression to fit ECG data
"""

import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

from load_train_cv_test import load_train_cv_test
from get_x_y import get_x_y
from log import logger

CACHE_DIR = '../cache/ptb_train_cv_test_sets'

if __name__ == '__main__':
    [trainSets, cvSets, testSets] = load_train_cv_test(CACHE_DIR)

    [train_x, train_y] = get_x_y(trainSets)
    logger.info('finish split x y from taining sets')

    [cv_x, cv_y] = get_x_y(cvSets)
    logger.info('finish split x y from cv sets')

    model = linear_model.LinearRegression()

    # training
    model.fit(train_x, train_y)
    print('Coefficients: \n', model.coef_)

    # predicting
    cv_predict = model.predict(cv_x)

    # mse
    print('mse: %.2f\n' % (np.mean((cv_predict - cv_y)**2)))

    # Explained variance score: 1 is perfect prediction
    print('Variance Socre: %.2f\n' % (model.score(cv_x, cv_y)))
