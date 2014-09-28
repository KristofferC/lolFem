"""
File that contains the class definition of a
boundary condition
"""

import logging
import math

logger = logging.getLogger(__name__)


class BoundaryCondition(object):

    """
    Base class for different boundary conditions.
    """

    def __init__(self, value, dof_ids, essential, set_applied_to=None):
        """
        Initiates a boundary class instance.


        Parameters
        ==========
        value : string or float
            This can be a string with python syntax that describes
            the value of the boundary condition as a function of
            space and time, (t,x,y,z). If the type of `value` is
            a float it will be interpreted as being a constant.
        dof_ids : list of ints
            Represents the dof ids the bc applies to.
        essential : bool
            Determines if the boundary condition is essential or not.
        set_applied_to : `lolFem.core.node_set.NodeSet` or lolFem.core.element_set.ElementSet
            Boundary conditions are applied to different types of sets depending
            on the nature of the boundary condition.

        Raises
        ======
        SetTypeError
            When applying a boundary condition to a set of the wrong type.

        See also
        ========
        lolFem.core.boundary_conditions.dirichlet.Dirichlet
        lolFem.core.boundary_conditions.point_load.PointLoad
        """

        # Some eval tricksing to create the function from the string.
        # This is so we don't have to parse the string every time
        # we want to evaluate the expression.
        def f_value(op):
            return eval("lambda t,x,y,z:" + str(op), math.__dict__)
        self.f_value = f_value(value)

        self.dof_ids = dof_ids
        self.essential = essential
        self.set_applied_to = set_applied_to

    def give_value(self, t, node):
        """
        Returns the value after bing scaled with `factor_func`

        Parameters
        ==========
        t : float
            Current time in analysis
        """
        x = node.give_coordinate(1)
        y = node.give_coordinate(2)
        z = node.give_coordinate(3)

        return self.f_value(t, x, y, z)

    def print_out(self, name):
        """
        Prints information about itself.

        Classes inheriting from `BoundaryCondition` calls this method
        in their `__str__` with their own name as argument.

        Parameters
        ==========
        name : string
            The name of the inheriting boundary condition
        """
        return "Boundary condition of type: {}, with n = {}, value = {}, dofids = {}".format(
            name,
            self.n,
            self._value,
            self.dof_ids)


class SetTypeError(Exception):

    """
    Exception to raise when a boundary condition is applied
    to the wrong type of set.
    """
    pass
