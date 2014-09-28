import logging

import numpy as np

from lolFem.interpolators.lin_trig_interp import LinTrigInterp
from lolFem.core.dof import D_u, D_v
from .element import Element
from lolFem.core.quadrature import GaussIntegration

logger = logging.getLogger(__name__)


class TrigPlaneStrain(Element):

    def __init__(self, n, vertices):
        interpolator = LinTrigInterp()
        n_gausspoints = 1
        integrator = GaussIntegration(n_gausspoints, "triangle")
        n_dofs = 6
        super(TrigPlaneStrain, self).__init__(n,
                                              vertices,
                                              interpolator,
                                              "TrigPlaneStrain",
                                              n_gausspoints,
                                              integrator,
                                              n_dofs)

    def give_dof_mask(self):
        return [D_u, D_v]

    def compute_B(self, gauss_point, nodes):
        dNdx = self.interpolator.eval_dNdx(
            gauss_point.local_coords,
            self.vertices,
            nodes)
        B = np.zeros((4, 6), dtype=np.float64)

        B[0, 0] = dNdx[0, 0]
        B[0, 2] = dNdx[1, 0]
        B[0, 4] = dNdx[2, 0]

        B[1, 1] = dNdx[0, 1]
        B[1, 3] = dNdx[1, 1]
        B[1, 5] = dNdx[2, 1]

        B[3, 0] = dNdx[0, 1]
        B[3, 1] = dNdx[0, 0]
        B[3, 2] = dNdx[1, 1]
        B[3, 3] = dNdx[1, 0]
        B[3, 4] = dNdx[2, 1]
        B[3, 5] = dNdx[2, 0]

        return B

    def compute_volume_around(self, gp, nodes):

        h = self.section.thickness
        det_J = abs(
            self.interpolator.give_det_J(
                gp.local_coords,
                self.vertices,
                nodes))

        return det_J * gp.weight * h

    # TODO: This code sucks
    def recover_fields_in_nodes(self, mesh):
        gp = self.integrator.gausspoints[0]
        for vert in self.vertices:
            node = mesh.nodes[vert]
            node.stress_vec.append(gp.material_status.stress)
            node.strain_vec.append(gp.material_status.strain)

    @property
    def vtk_class(self):
        import vtk
        return vtk.vtkTriangle()
