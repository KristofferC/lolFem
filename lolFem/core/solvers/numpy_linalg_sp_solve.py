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

    def solve(self, model, t):
        # Compute element stiffness matrices and assemble into global
        K = model.domain.assemble_stiffness_matrix()
        # Compute applied loads
        load = model.domain.compute_load_vector(0)

        # Compute internal forces (from ex. Dirichlet bc).
        internal_forces = model.domain.assemble_internal_forces(t)
        # Resulting force vector
        f = load - internal_forces

        # Solve system
        u = self.solve_eq(K, f)

        # Propagate updated unknowns to free dofs
        model.domain.update_dof_values(u, t)

        # Recalculate internal forces to display the residual
        internal_forces = model.domain.assemble_internal_forces(t)
        f_tot = load - internal_forces

        residual = np.linalg.norm(
            sum(np.abs(f_tot)) / sum(np.sqrt(load ** 2 + internal_forces ** 2)))
        print "\t\tResidual: " + str(residual)


    def solve_eq(self, K, f):
        return spsolve(K, f)
