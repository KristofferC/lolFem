import logging

import numpy as np

from .interpolator import Interpolator
from lolFem.core.mt_tools import determinant_2x2, inv_2x2

logger = logging.getLogger(__name__)


class LinTrigInterp(Interpolator):

    # Shape functions in local coordinates
    def eval_N(self, local_coords):
        N = np.zeros(3, dtype=np.float64)
        ksi = local_coords[0]
        eta = local_coords[1]

        N[0] = ksi
        N[1] = eta
        N[2] = 1.0 - ksi - eta

        return N

    def give_area(self, vertices, mesh):
        [x1, x2, x3, y1, y2, y3] = self._give_cords(vertices, mesh)
        return 0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    def eval_dNdx(self, local_coords, vertices, mesh):

        dN = self.give_derivatives(local_coords)
        J = self.give_J(local_coords, vertices, mesh)
        J_inv = inv_2x2(J)
        dNdx = dN.dot(J_inv.transpose())

        return dNdx

    def give_derivatives(self, local_coordinates):

        dN = np.zeros((3, 2), dtype=np.float64)

        # Derivative w.r.t ksi
        dN[0, 0] = 1.0
        dN[1, 0] = 0.0
        dN[2, 0] = -1.0

        # Derivative w.r.t eta
        dN[0, 1] = 0.0
        dN[1, 1] = 1.0
        dN[2, 1] = -1.0

        return dN

    def give_det_J(self, local_coords, vertices, mesh):
        J = self.give_J(local_coords, vertices, mesh)
        return determinant_2x2(J)

    def give_J(self, local_coords, vertices, mesh):

        J = np.zeros((2, 2), dtype=np.float64)
        dN = self. give_derivatives(local_coords)

        for row in xrange(0, 3):
            x = mesh.nodes[vertices[row]].coordinates[0]
            y = mesh.nodes[vertices[row]].coordinates[1]

            J[0, 0] += dN[row, 0] * x
            J[0, 1] += dN[row, 0] * y
            J[1, 0] += dN[row, 1] * x
            J[1, 1] += dN[row, 1] * y

        return J

    def local_to_global(self, local_coords, vertices, mesh):
        global_coords = np.zeros((3, 1), dtype=np.float64)

        # Using same functions for interpolating coordinates as
        # interpolating fields
        N = self.eval_N(local_coords)

        [x1, x2, x3, y1, y2, y3] = self._give_cords(vertices, mesh)

        global_coords[0] = N.dot([x1, x2, x3])
        global_coords[1] = N.dot([y1, y2, y3])

        return global_coords

    def global_to_local(self, global_coords, vertices, mesh):
        local_coords = np.zeros((3, 1), dtype=np.float64)

        [x1, x2, x3, y1, y2, y3] = self._give_cords(vertices, mesh)
        detJ = self.give_det_J(local_coords, vertices, mesh)

        local_coords[0] = ((x2 * y3 - x3 * y2) + (y2 - y3) *
                           global_coords[0] + (x3 - x2) * global_coords[1]) / detJ
        local_coords[1] = ((x3 * y1 - x1 * y3) + (y3 - y1) *
                           global_coords[0] + (x1 - x3) * global_coords[1]) / detJ

    def _give_cords(self, vertices, mesh):
        return([mesh.nodes[vertices[0]].coordinates[0],
                mesh.nodes[vertices[1]].coordinates[0],
                mesh.nodes[vertices[2]].coordinates[0],
                mesh.nodes[vertices[0]].coordinates[1],
                mesh.nodes[vertices[1]].coordinates[1],
                mesh.nodes[vertices[2]].coordinates[1]])
