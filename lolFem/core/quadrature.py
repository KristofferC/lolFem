"""
File to hold the GaussPoint and GaussIntegration
classes
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


class GaussPoint(object):

    def __init__(self, local_coords, weight):
        """
        local_coords : numpy.ndarray
        weight : numpy.core.multiarray.dtype
        """
        self.local_coords = local_coords
        self.weight = weight

        self.material_status = None

    def update(self):
        """
        Updates the material status in the gauss points.
        """
        self.material_status.update()


class GaussIntegration(object):

    """
    The gauss integration scheme[1] is used to estimate
    the integrals over the elements.

    An element creates a `GaussIntegration` class which
    contains the gauss points and the coordinates and
    weights for the gauss points.

    .. [1] http://en.wikipedia.org/wiki/Gaussian_quadrature
    """

    def __init__(self, n_gps, elem_type):
        """
        Creates a `GaussIntegration` class.

        A `GaussIntegration` class consists of a collection
        of gauss points.

        Parameters
        ==========

        n_gps: int
            The number of gauss points to use to
            integrate functions on the element.
        elem_type: str
            The element type, used together with
            `n_gps` to give the coordinates and
            weight of the gauss points.
        """
        self.gausspoints = []

        # Fetch the coordinates and weights for the gauss points
        [coords, weights] = self.get_coords_and_weight(n_gps, elem_type)
        for weight, coord in zip(weights, coords):
            self.gausspoints.append(GaussPoint(coord, weight))

    def get_coords_and_weight(self, n_gps, elem_type):
        """
        Gets the coordinates and weights for the gauss points
        associated with the element.

        Depending on the element type and how many integration
        points are used there is a different collection
        of coordinates and weights used for the gauss points.
        This method looks them up in a table.

        Parameters
        ==========
        n_gps : int
            The number of gauss points the element uses.
        element_type : string
            The type of element


        Raises
        ======
        NoData
            If there is no data for the combination
            of element type and number of gauss points.

        Returns
        =======
        List
            The first item is a n_gps x n_dim numpy array
            where the n:th row gives the coordinates for the
            n:th gauss points. The second item is a n_gps x 1
            numpy array where the n:th value is the weight
            for the n:th gauss points.
        """

        if elem_type == "triangle":
            if n_gps == 1:
                coords = [[1.0 / 3.0, 1.0 / 3.0]]
                weights = [0.5]

        elif elem_type == "quadraterial":
            if n_gps == 4:
                coords = np.array([[-1 / np.sqrt(3), -1 / np.sqrt(3)],
                                   [1 / np.sqrt(3), -1 / np.sqrt(3)],
                                   [1 / np.sqrt(3), 1 / np.sqrt(3)],
                                   [-1 / np.sqrt(3), 1 / np.sqrt(3)]])
                weights = np.array([1.0, 1.0, 1.0, 1.0])
        else:
            raise NoData("No data for that combination of number "
                         "of gausspoints and element type")

        return [coords, weights]

    def update(self):
        """
        Propagate the update command to the gauss points.
        """
        for gp in self.gausspoints:
            gp.update()


class NoData(Exception):

    """
    Exception to raise when there is no data
    available for the element type, number of gauss points
    combination.
    """
    pass
