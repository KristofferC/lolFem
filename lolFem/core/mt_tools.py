"""
Contains different operations to apply
to matrices / tensors.
"""

import numpy as np


def determinant_2x2(A):
    """
    Calculates the determinant for a 2x2 matrix
    by explicit formula.

    Parameters
    =========
    A : numpy.ndarray
        2x2 matrix

    Returns
    ======
    float
    """
    return A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]


def inv_2x2(A):
    """
    Calculates the inverse for a 2x2 matrix
    by explicit formula.

    Parameters
    =========
    A : numpy.ndarray
        2x2 matrix

    Returns
    ======
    float
    """
    det = determinant_2x2(A)
    return 1.0 / det * np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])
