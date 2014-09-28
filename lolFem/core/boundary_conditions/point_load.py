"""
File that contains the class definition of a
point load
"""

import logging

from lolFem.core.boundary_conditions.boundary_condition import BoundaryCondition, SetTypeError
from lolFem.core.node_set import NodeSet

logger = logging.getLogger(__name__)


class PointLoad(BoundaryCondition):

    """
    A point load represents a force applied at a single infinitesimal point.
    """

    def __init__(self, value, dof_ids, set_applied_to):

        # First check if set is of correct type
        if not isinstance(set_applied_to, NodeSet):
            raise SetTypeError(
                "It is only possible to apply point loads to node sets.")
        essential = False

        # Call base boundary condition, with the flag that
        # this is not an essential bc.
        super(PointLoad, self).__init__(value,
                                        dof_ids,
                                        essential,
                                        set_applied_to)

    def __str__(self):
        return super(PointLoad, self).print_out("Point Load")
