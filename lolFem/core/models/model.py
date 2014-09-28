"""
File to hold the Model base class.
"""

from abc import ABCMeta, abstractmethod
import logging

import numpy as np

logger = logging.getLogger(__name__)


class Model(object):
    __metaclass__ = ABCMeta

    def __init__(self, solver, domain, timer, vtk_file_name=None):
        """
        Initiates a model class instance.

        Parameters
        ==========
        solver : `lolFem.core.solvers.solver`
            The solver to use in the analysis.
        domain : `lolFem.core.domain.Domain`
            The domain in the model.
        time : list of floats
            The times to run the analysis over.
        vtk_file_name : string, optional
            File name to export results to in each time step.
            If not given, no data is exported.
        """
        self.domain = domain
        self.solver = solver
        self.number_of_prescribed_equations = 0
        self.number_of_equations = 0
        for element in domain.mesh.elements.values():
            element.model = self

        self.domain.model = self
        self.timer = timer
        self.vtk_file_name = vtk_file_name
        self. f = None

    def go(self):
        """
        Startes the analysis.

        This is done by first creating the dofs, then assigning
        the dofs their numbers, then creating the needed
        material statuses, and then starts the solver.
        """
        self.check()
        self.domain.create_dofs()
        self.domain.set_dof_numbering()
        self.domain.create_material_statuses()
        self.solve(self)

        # loop time steps, for now only 1 step

    def check(self):
        """
        This should check if everything looks fine so we don't
        get ugly error messages.
        """

        # TODO: Add more stuff here

        # Check if all elements has sections assigned to them
        logger.debug("Checking section assignments..")
        for element_id in self.domain.mesh.elements:
            element = self.domain.mesh.elements[element_id]
            no_section_element_ids = []
            if element.section is None:
                no_section_element_ids.append(element_id)
        if not len(no_section_element_ids) == 0:
            raise NoSectionError(
                "Error: Elements with the following ids"
                "have no section: {}".format(no_section_element_ids))

        logger.debug("Checks completed...")

    @abstractmethod
    def solve(self):
        pass

    # Propagate update to domain
    def update(self):
        """
        Propagates the update command to the domain.
        """
        self.domain.update()

    def export_to_vtk(self, filename):
        """

        Parameters
        =========
        filename : string
            The filename of the file to export
            data to.
        """
        from lolFem.visualization import vtk_tools
        self.domain.recover_fields_in_nodes()
        vtk_tools.write_vtk_file(self.domain.mesh, filename)


class NoSectionError(Exception):

    """
    Raised if an element does not have
    a section assigned to it.
    """
    pass
