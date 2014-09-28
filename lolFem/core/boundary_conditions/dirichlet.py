"""
File that contains the class definition for a Dirichlet
boundary condition
"""

import logging

from lolFem.core.boundary_conditions.boundary_condition import BoundaryCondition, SetTypeError
from lolFem.core.node_set import NodeSet

logger = logging.getLogger(__name__)


class Dirichlet(BoundaryCondition):

    """
    Class describing a Dirichlet boundary condition[1].

    A Dirichlet boundary conditions (bc) means that the solution at needs
    to take the value of the bc where it is applied.
    If a Dirichlet bc is applied to a dof, the dof's value will therefore
    always be equal to that of the Dirichlet bc.

    .. [1] http://en.wikipedia.org/wiki/Dirichlet_boundary_condition
    """

    def __init__(self, value, dof_ids, set_applied_to):

        # Check if set is of correct type
        if not isinstance(set_applied_to, NodeSet):
            raise SetTypeError(
                "It is only possible to apply dirichlet boundary conditions"
                " to node sets.")

        # Call base boundary condition, with the flag that
        # this is an essential bc.
        essential = True
        super(
            Dirichlet,
            self).__init__(value,
                           dof_ids,
                           essential,
                           set_applied_to)
        self.req_active = True

    def __str__(self):
        return super(Dirichlet, self).print_out("Dirichlet")
