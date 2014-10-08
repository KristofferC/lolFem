# cython: profile=True
"""
File to hold `Element` class
"""

from abc import ABCMeta, abstractmethod
import logging

import numpy as np

from lolFem.core.dof import DT_master
from lolFem.core.quadrature import GaussIntegration

import cython
cimport numpy as np

DTYPE = np.float64

ctypedef np.float64_t DTYPE_t

logger = logging.getLogger(__name__)


class Element(object):

    """
    Represents a finite element.
    """
    __metaclass__ = ABCMeta

    def __init__(
            self,
            n,
            vertices,
            interpolator,
            element_name,
            n_gausspoints,
            integrator,
            n_dofs):
        """
        Initiates an instance of the `Element` class.

        Parameters
        ==========
        n: int
            Unique element identifier
        vertices: list
            The vertices of the element consists of the node
            identifiers
        interpolator: lolFem.interpolators.interpolator.Interpolator
            Method used to interpolate functions in the element.
        element_name: str
            The name of the element.
        n_gausspoints: int
            The number of gauss points used for the
            gauss quadrature integration
        integrator: lolFem.core.quadrature.GaussIntegration
            A gauss integrator scheme
        n_dofs: int
            The number of dofs in the element
        """
        self.n = n
        self.vertices = vertices
        self.element_name = element_name
        self.interpolator = interpolator
        self.n_gausspoints = n_gausspoints
        self.n_dofs = n_dofs
        self.domain = None
        self.section = None
        self.model = None

        self.integrator = integrator

    def __str__(self):
        return ("Element of type {0} containing the vertices with "
                "id {1}.".format(self.element_name, self.vertices))

    @abstractmethod
    def compute_B(self, gauss_point, nodes):
        """
        Computes the B-matrix for the element.

        Derivative of the shape functions such that
        epsilon = B * a, where a = [a1_x, a1_y, a1_z, a2_x, ..]

        Parameters
        ==========
        gauss_point : lolFem.core.quadrature.GaussPoint
            The gauss point to calculate the B-matrix in.
        nodes : list of nodes
            The nodes in the mesh.
        """
        pass

    @abstractmethod
    def compute_volume_around(self, gp, nodes):
        """
        Computes the weight for the term.



        Parameters
        ===========
        gauss_point : lolFem.core.quadrature.GaussPoint
            The gauss point to calculate the B-matrix in.
        nodes : list of nodes
            The nodes in the mesh.
        """
        pass

    @abstractmethod
    def give_dof_mask(self):
        """
        Gives the physical interpretation of the dofs.

        These are currently identified as ints, the different
        types are listed in the `Dof` class file.
        """
        pass

    def create_material_statuses(self):
        """
        Creates the material statuses in the gauss points.

        Loops over the gauss points and gives them all a
        material status depending on what material is
        defined for the section of the element.
        """
        for gp in self.integrator.gausspoints:
            gp.material_status = self.section.material.create_material_status()

    @cython.boundscheck(False)
    def compute_stiffness_matrix(self, mesh):
        """
        Computes the element stiffness matrix.

        This is done by gauss quadrature where we
        sum weighted values of the function at
        discrete points in the element.

        .. math:: \mathbf{K}_e = \sum_{i} \mathbf{B}^T \mathbf{D} \mathbf{B} w_i
        """
        cdef int n_dofs = self.n_dofs
        cdef np.ndarray[DTYPE_t, ndim=2] Ke = np.zeros(
            (n_dofs,
             n_dofs),
            dtype=np.float64)

        cdef np.ndarray[DTYPE_t, ndim=2] Be
        cdef np.ndarray[DTYPE_t, ndim=2] De
        cdef double dV
        for gp in self.integrator.gausspoints:

            Be = self.compute_B(gp, mesh)
            De = self.compute_constitutive_matrix(gp)
            dV = self.compute_volume_around(gp, mesh)

            # And this is why .dot is stupid dotdottelidottdott:
            # Ke = int B^t D B dv
            Ke += np.transpose(Be).dot(De.dot(Be)) * dV
        return Ke

    def compute_constitutive_matrix(self, gp):
        """
        Computes the consitutive matrix, 'D', for the element.

        Returns
        =======
        numpy.ndarray
            The constitutive matrix.
        """
        material = self.section.material
        return material.give_stiffness_matrix_plane_strain(gp)

    def compute_unknown(self, t):
        """
        Computes the values of the dofs
        for the element.

        Parameters
        ==========
        t : float
            The current time in the analysis

        Returns
        =======
        list of floats
            The values of all dofs in the element.
        """

        u = []
        for vert in self.vertices:
            node = self.domain.mesh.nodes[vert]
            for dof in node.dofs:
                if dof.dof_type == DT_master:
                    u.append(dof.value)
                else:
                    bc = self.domain.dof_bc[node.n].get(dof.dof_id)
                    u.append(bc.give_value(t, node))
        return u

    def compute_internal_forces(self, t):
        """
        Computes the internal forces in the element.

        Parameters
        ==========
        t : float
            The current time in the analysis

        Returns
        =======
        list of floats
            The internal forces
        """
        f_int = np.zeros(self.n_dofs, dtype=np.float64)
        u = self.compute_unknown(t)
        for gp in self.integrator.gausspoints:
            B = self.compute_B(gp, self.domain.mesh)

            strain = B.dot(u)

            # This will also set stress + strain in temp variables
            # in gp material status
            stress = self.section.material.compute_stress(strain, gp)

            dV = self.compute_volume_around(gp,
                                            self.domain.mesh)
            # f = B^t * sigma * dv
            f_int += B.transpose().dot(stress) * dV

        return f_int

    def compute_strain(self, gp):
        """
        Computes strain in a gauss point.

        .. math: \epsilon = \mathbf{B}\mathbf{u}

        Parameters
        ==========
        gp : lolFem.core.quadrature.GaussPoint
            The gauss point to calculate the strain in.

        Returns
        =======
        list of floats
            The strain in Voigt format [e_xx, e_yy, e_zz,
            e_xy,..
        """
        # TODO: Check voigt format
        B = self.compute_B(gp, self.domain.mesh)
        u = self.compute_unknown()

        return B.dot(u)

    def recover_fields_in_nodes_2(self, mesh):
        T = np.zeros((len(self.vertices),
                      self.n_gausspoints),
                     dtype=np.float64)
        # TODO: Fix hardcoded 4
        w_stress = np.zeros((self.n_gausspoints, 4), dtype=np.float64)
        w_strain = np.zeros((self.n_gausspoints, 4), dtype=np.float64)
        for i, gp in enumerate(self.integrator.gausspoints):
            # For each gauss point add its reciprocal coordinate to list.
            # This is the local coordinates for the node if we look at the
            # gauss points as making up an element
            prim_coords = np.reciprocal(gp.local_coords)
            T[:, i] = self.interpolator.eval_N(prim_coords)
            w_stress[i, :] = gp.material_status.stress
            w_strain[i, :] = gp.material_status.strain

        # This will be matrices with columns as the node index and row as the
        # field component
        stress_node = T.dot(w_stress)
        strain_node = T.dot(w_strain)

        for i, vert in enumerate(self.vertices):
            node = mesh.nodes[vert]
            node.stress_vec.append(stress_node[i, :])
            node.strain_vec.append(strain_node[i, :])

    def update(self):
        """
        Propagates update to the integrator.
        """
        self.integrator.update()
