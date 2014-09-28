"""
File that contains the class definition of a
dof
"""

import logging

logger = logging.getLogger(__name__)

# Dof ids
D_u = 1
D_v = 2
D_w = 3


# Dof types
DT_master = 1
DT_active = 2


class Dof(object):

    """
    A degree of freedom a parameter that describes the system. They
    are numbers with different physical meanings that enters
    the equations we are trying to solve.
    """

    def __init__(self, n, node, dof_type, dof_id, equation_number=0, value=0):
        """
        Creates a dof instance.

        Parameters
        =========

        n : int
            Unique number to identify the dof.
        node : lolFem.core.node.Node
            The node that the dof is associated to.
        dof_type : int
        dof_id : {D_u, D_v, D_w}
            Describes what type of physical meaning the dof has,
            e.g displacement in x-direction. Right now, only
            displacements are supported.
        equation_number : int
            The equation number of the dof. If this is a positive
            number then the dof is not constrained by an essential
            boundary condition and it is thus one of the unknowns
            to solve for. If `equation_number` is negative it is
            restricted by an essential boundary condition and its
            `value` will be determined by the acting boundary condition.
            This variable is not set at creation of the dof but later
            by the `lolFem.core.domain.set_dof_numbering` method.
        value : float
            The value of the dof.
        """
        self.n = n
        # TODO: Does dof need to know what node owns it?
        self.node = node
        self.dof_type = dof_type
        self.dof_id = dof_id
        self.equation_number = 0
        self.value = 0

    def update(self):
        """
        Does nothing right now, should go into boundary condition
        and fetch its new value.
        """
        pass

    def __str__(self):
        return "Dof for node {} of type {} with id {}.".format(
            self.node.n,
            self.dof_type,
            self.dof_id)
