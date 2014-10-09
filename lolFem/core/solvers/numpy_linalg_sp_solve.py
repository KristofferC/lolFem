"""
File for the NumpyLinalgSpSolve class
"""
import logging

from scipy.sparse.linalg import spsolve
import numpy as np

from lolFem.core.solvers.solver import Solver

logger = logging.getLogger(__name__)


class NumpyLinalgSpSolve(Solver):

    """
    The `NumpyLinalgSpSolve` class is the solver
    that uses the built in Scipy-solver for the linear
    equation system Ax = b where A is sparse in
    Scipy's own format.
    """

    def __init__(self):
        pass

    def solve(self, K, f):
        return spsolve(K, f)
