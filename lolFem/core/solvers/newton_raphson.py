import logging

import numpy as np

from lolFem.core.solvers.solver import Solver
from .numpy_linalg_sp_solve import NumpyLinalgSpSolve
from lolFem import logger

logger = logging.getLogger(__name__)


class Newton(Solver):

    """
    Implements a full Newton-Raphson solver. No line searching is done.
    """

    def __init__(self, rel_tol, miter, f_to_break=10e-4):
        """
        Initiates a `Newton` solver class

        rel_tol: float
            If the relative residual is lower than this
            number we consider it having converged.
        miter: int
            Max number of iterations before exiting
            iterations for the current time step.
        f_to_break: float
            If the total forces on the system is very low
            we might be in a rigid body motion case.
            In that case, do one newton iteration and exit.
            This value determines the limit for this scenario.
        """
        self.linear_solver = NumpyLinalgSpSolve()
        self.tol = rel_tol
        self.miter = miter
        self.f_to_break = f_to_break

    def solve(self, model, t):
        """
        Attempts to solve the force equilibrium equations
        for the current time step.

        Parameters
        =========
        model : lolFem.core.models.Model
            The model to solve equations for.
        time : float
            The current time in the analysis.
        """

        print t

        # Compute applied loads, this should be independent of deformation
        load, load_squared = model.domain.compute_load_vector(t)
        iteration = 0
        while True:
            if iteration > self.miter:
                print "Max iterations achived, exiting"
                logging.warning(
                    "Max iteration achieved with resiudal %s.",
                    residual)
                break

            # Calculate internal forces.
            internal_forces, internal_forces_squared = model.domain.assemble_internal_forces(t)
            f_tot = load - internal_forces

            residual = np.sqrt(f_tot.dot(f_tot)) / np.sqrt(np.sum(internal_forces_squared + load_squared))

            print "\t\tIteration {}, relative residual {}".format(iteration, residual)

            if residual < self.tol:
                print "\t\tConverged!"
                break

            # Low total forces
            if f_tot.dot(f_tot) < self.f_to_break:
                # TODO: Make this nicer
                #u = self.linear_solver.solve_eq(K, f_tot)
                #model.domain.update_dof_values(u, t)
                #model.domain.assemble_internal_forces(t)
                print "\t\tSmall external forces: {}, assuming equilibrium.".format(sum(np.abs(load)))
                break

            # Full Newton, update stiffness matrix
            K = model.domain.assemble_stiffness_matrix()

            # Solve for unknowns
            du = self.linear_solver.solve_eq(K, f_tot)

            print "du"
            print du

            # Propagate new unknowns back to dofs.
            model.domain.update_dof_values(du, t)

            iteration += 1


        model.f = internal_forces
