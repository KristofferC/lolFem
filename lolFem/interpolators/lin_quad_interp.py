import logging

import numpy as np

from .interpolator import Interpolator
from lolFem.core.mt_tools import determinant_2x2, inv_2x2

logger = logging.getLogger(__name__)


class LinQuadInterp(Interpolator):

    def __init__(self):
        pass

    # Shape functions in local coordinates
    def eval_N(self, local_coords):
        N = np.zeros(4, dtype=np.float64)
        ksi = local_coords[0]
        eta = local_coords[1]

        N[0] = (1.0 + ksi) * (1.0 + eta) * 0.25
        N[1] = (1.0 - ksi) * (1.0 + eta) * 0.25
        N[2] = (1.0 - ksi) * (1.0 - eta) * 0.25
        N[3] = (1.0 + ksi) * (1.0 - eta) * 0.25

        return N

    def eval_dNdx(self, local_coords, vertices, mesh):
        """

        :type local_coords: numpy.ndarray
        :type vertices: list
        :type mesh: lolFem.core.mesh.Mesh
        :return: :rtype:
        """
        dN = self.give_derivatives(local_coords)
        J = self.give_J(local_coords, vertices, mesh)
        J_inv = inv_2x2(J)
        dNdx = dN.dot(J_inv.transpose())

        return dNdx

    def give_area(self, vertices, mesh):
        [x1, x2, x3, x4, y1, y2, y3, y4] = self._give_cords(vertices, mesh)
        return abs(0.5 * ((x1 - x3) * (y2 - y4) - (x2 - x4) * (y1 - y3)))

    def give_J(self, local_coords, vertices, mesh):

        J = np.zeros((2, 2), dtype=np.float64)
        dN = self.give_derivatives(local_coords)

        for row in xrange(0, 4):
            x = mesh.nodes[vertices[row]].coordinates[0]
            y = mesh.nodes[vertices[row]].coordinates[1]

            J[0, 0] += dN[row, 0] * x
            J[0, 1] += dN[row, 0] * y
            J[1, 0] += dN[row, 1] * x
            J[1, 1] += dN[row, 1] * y

        return J

    def give_det_J(self, local_coords, vertices, mesh):
        J = self.give_J(local_coords, vertices, mesh)
        return determinant_2x2(J)

    def give_derivatives(self, local_coords):
        """

        :type local_coords: numpy.ndarray
        :return:
        :rtype: numpy.ndarray
        """
        ksi = local_coords[0]
        eta = local_coords[1]

        dN = np.zeros((4, 2), dtype=np.float64)

        # Derivative w.r.t ksi
        dN[0, 0] = 0.25 * (1.0 + eta)
        dN[1, 0] = -0.25 * (1.0 + eta)
        dN[2, 0] = -0.25 * (1.0 - eta)
        dN[3, 0] = 0.25 * (1.0 - eta)

        # Derivative w.r.t eta
        dN[0, 1] = 0.25 * (1.0 + ksi)
        dN[1, 1] = 0.25 * (1.0 - ksi)
        dN[2, 1] = -0.25 * (1.0 - ksi)
        dN[3, 1] = -0.25 * (1.0 + ksi)

        return dN

    def local_to_global(self, local_coords, vertices, mesh):

        global_coords = np.zeros((3, 1), dtype=np.float64)

        N = self.eval_N(local_coords)

        [x1, x2, x3, x4, y1, y2, y3, y4] = self._give_cords(vertices, mesh)

        global_coords[0] = N.dot([x1, x2, x3, x4])
        global_coords[1] = N.dot([y1, y2, y3, y4])

        return global_coords

    def global_to_local(self, global_coords, vertices, mesh):
        raise NotImplemented(
            "lin_quad_interp.global_to_local not implemented yet.")

    def _give_cords(self, vertices, mesh):
        return([mesh.nodes[vertices[0]].coordinates[0],
                mesh.nodes[vertices[1]].coordinates[0],
                mesh.nodes[vertices[2]].coordinates[0],
                mesh.nodes[vertices[3]].coordinates[0],
                mesh.nodes[vertices[0]].coordinates[1],
                mesh.nodes[vertices[1]].coordinates[1],
                mesh.nodes[vertices[2]].coordinates[1],
                mesh.nodes[vertices[3]].coordinates[1]])


class NotImplemented(Exception):
    pass
