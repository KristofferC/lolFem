import logging

import numpy as np

from .material import Material
from .material_status import MaterialStatus

logger = logging.getLogger(__name__)


class LinearIsotropic(Material):

    def __init__(self, e, nu):
        # Modulus of elasticity
        self.E = e

        # Poisson ratio
        self.nu = nu

        # Modulus of shear
        self.G = self.E / (2.0 * (1.0 + self.nu))

    def create_material_status(self):
        return LinearIsotropicMaterialStatus()

    def give_stiffness_matrix_1d(self):
        k = np.zeros((1, 1), dtype=np.float64)
        k[0, 0] = self.E

        return k

    def give_stiffness_matrix_plane_strain(self, gp, time_assistant):
        k = np.zeros((4, 4), dtype=np.float64)

        factor = self.E / ((1.0 + self.nu) * (1.0 - 2.0 * self.nu))

        k[0, 0] = factor * (1.0 - self.nu)
        k[1, 1] = factor * (1.0 - self.nu)
        k[2, 2] = factor * (1.0 - self.nu)
        k[3, 3] = self.G

        k[0, 1] = factor * self.nu
        k[0, 2] = factor * self.nu
        k[1, 0] = factor * self.nu
        k[1, 2] = factor * self.nu
        k[2, 0] = factor * self.nu
        k[2, 1] = factor * self.nu

        return k

    def compute_stress(self, strain, gp, time_assistant):
        D = self.give_stiffness_matrix_plane_strain(gp, time_assistant)
        stress = D.dot(strain)
        gp.material_status.temp_stress = stress
        gp.material_status.temp_strain = strain
        return stress


class LinearIsotropicMaterialStatus(MaterialStatus):

    def __init__(self):
        super(LinearIsotropicMaterialStatus, self).__init__()
