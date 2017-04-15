#!/usr/bin/env python

import numpy as np

def get_x_y(sets):
    """
    sets is a numpy.array
        [
            [1,2,...,2000, 1],
            [1,2,...,2000, 0],
        ]
    """
    col = sets.shape[1] - 1
    x = sets[:, 0:col]
    y = sets[:, col, np.newaxis]
    """
    print sets.shape
    print x.shape
    print y.shape
    """
    return [x, y]
