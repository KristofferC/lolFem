"File to hold the NodeSet class"

import logging

logger = logging.getLogger(__name__)


class NodeSet(object):

    """
    Represents a set of nodes
    """

    def __init__(self, name, ids=None):
        """
        Initiates a node set class.

        Parameters
        ==========
        name : string
            The name of the node set.
        ids : list of ints
            The node identifers in the node set.
        """
        self.name = name

        #: The nodes contained in the set
        if ids is None:
            ids = []
        self.ids = ids

    def give_node_ids(self):
        """
        Gives all the node identifiers in the set.

        Returns
        =======
        list of ints
        """
        return self.ids

    def __str__(self):
        return("Node set with name {0} containing nodes with the "
               "following ids {1}".format(self.name, self.ids))
