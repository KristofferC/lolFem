"""
File to contain Section class definition.
"""

import logging

logger = logging.getLogger(__name__)


class Section(object):

    """
    A section is a subset of the elements in a mesh.
    It describes what material is used for those
    elements and the thickness in cases of assumption
    of plane strain/stress.

    At analysis all elements need to have one and
    only one section assigned to them.
    """

    def __init__(self, material, thickness=0.0):
        """
        material: lolFem.materials.Material
            The material to use in the section
        thickness : float
            Thickness in case of plane strain/stress assumption
        """
        self.material = material
        self.thickness = thickness

    def assign_to(self, mesh, element_set):
        """
        Assigns the section to an element set.

        Parameters
        ==========
        mesh : lolFem.core.mesh.Mesh
            The mesh
        element_set : lolFem.core.element_set.ElementSet
            The element set in the mesh to assign
            the section to.
        """
        for element_id in element_set.ids:
            element = mesh.elements[element_id]
            element.section = self
