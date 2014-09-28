"""
File to cotain the ElementSet class.
"""

import logging

logger = logging.getLogger(__name__)


class ElementSet(object):

    """ Represents a set of elements"""

    def __init__(self, name, ids=None):
        """
        Initiates an element set.

        Parameters
        ==========
        name : string
            The name of the element set
        ids : list of ints
            The identifiers of the elements in the set
        """
        self.name = name

        if ids is None:
            ids = []
        self.ids = ids

    def __str__(self):
        """
        Returns a string representation of the element set.
        """
        return ("Element set with name {0} containing elements with the "
                "following ids {1}".format(self.name, self.ids))
