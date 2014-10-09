"""
File to hold the Node class
"""
import logging

logger = logging.getLogger(__name__)


class Node(object):

    """
    Nodes are discrete points in space where we calculate values of
    unknowns in our problem (for example displacements).
    """

    def __init__(self, n, coordinates, dofs=None):
        """
        Initiates a Node class.

        n : int
            Unique identifer for the node
        coordinates : list of floats
            The coordinates in space
            for the node in x, y, (z) order
        dofs: List of `Dof` instances.
            The dofs in the node
        """
        self.coordinates = coordinates
        self.n = n
        if dofs is None:
            dofs = []
        self.dofs = dofs
        self.displacements = 0

        # TODO: Fix hardcoding for fields
        self.stress_vec = []
        self.strain_vec = []

        self.strain = None
        self.stress = None

    def give_coordinate(self, i):
        """
        i : {1, 2, 3}
           The i:th component to return,
           defaults to 0.0 if the node only
           has two components.

        Returns
        =======
        float
            The spatial component of the node
        """
        if i > len(self.coordinates):
            return 0.0
        return self.coordinates[i - 1]

    def update(self):
        """
        Propagate the update command
        to all dofs.
        """
        self.stress_vec = []
        self.stress_vec = []
        for dof in self.dofs:
            dof.update()

    def __str__(self):
        return (
            "Node with id {} located at {}.".format(
                self.n,
                self.coordinates))
