"""
File to hold the `Interpolator` class
"""

from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger(__name__)


class Interpolator(object):

    """
    The `Interpolator class` is used to interpolate


    It consists of a
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def eval_N(self, local_coords):
        pass

    @abstractmethod
    def eval_dNdx(self, local_coords, vertices, mesh):
        pass

    @abstractmethod
    def give_J(self, local_coords, vertices, mesh):
        pass
