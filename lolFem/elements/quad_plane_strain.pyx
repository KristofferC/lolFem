# cython: profile=True

import logging

cimport numpy as np
import cython
import numpy as np

from lolFem.interpolators.lin_quad_interp import LinQuadInterp
from lolFem.core.dof import D_u, D_v
from .element import Element
from lolFem.core.quadrature import GaussIntegration

logger = logging.getLogger(__name__)

DTYPE = np.float64

ctypedef np.float64_t DTYPE_t

class QuadPlaneStrain(Element):

    def __init__(self, n, vertices):
        interpolator = LinQuadInterp()
        n_gausspoints = 4
        integrator = GaussIntegration(n_gausspoints, "quadraterial")
        n_dofs = 8
        super(QuadPlaneStrain, self).__init__(n,
                                              vertices,
                                              interpolator,
                                              "QuadPlaneStrain",
                                              n_gausspoints,
                                              integrator,
                                              n_dofs)

    def give_dof_mask(self):
        return [D_u, D_v]

    @cython.boundscheck(False)
    def compute_B(self, gauss_point, mesh):
        cdef np.ndarray[DTYPE_t, ndim=2] dNdx = self.interpolator.eval_dNdx(
            gauss_point.local_coords,
            self.vertices,
            mesh)
        cdef np.ndarray[DTYPE_t, ndim=2] B = np.zeros((4, 8), dtype=np.float64)

        cdef int i
        for i in range(0, 4):
            B[0, 2 * i] = dNdx[i, 0]
            B[1, 2 * i + 1] = dNdx[i, 1]

            B[3, 2 * i] = dNdx[i, 1]
            B[3, 2 * i + 1] = dNdx[i, 0]

        return B

    def compute_volume_around(self, gp, nodes):

        h = self.section.thickness
        det_J = abs(self.interpolator.give_det_J(gp.local_coords,
                                                 self.vertices,
                                                 nodes))

        return det_J * gp.weight * h

    # TODO: This code sucks
    def recover_fields_in_nodes(self, mesh):
        for i, vert in enumerate(self.vertices):
            node = mesh.nodes[vert]
            gp = self.integrator.gausspoints[i]
            node.stress_vec.append(gp.material_status.stress)
            node.strain_vec.append(gp.material_status.strain)

    @property
    def vtk_class(self):
        import vtk
        return vtk.vtkQuad()
