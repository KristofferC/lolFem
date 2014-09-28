import logging

import numpy as np

from material import Material
from material_status import MaterialStatus

logger = logging.getLogger(__name__)


class J2Plasticity(Material):

    def __init__(self, sig_y, Y, linear_material):
        self.sig_y = sig_y
        self.k = Y / np.sqrt(3.0)
        self.linear_material = linear_material

    def create_material_status(self):
        return J2PlasticityMaterialStatus()

    def compute_yield_func(self):
        J_2 =
        alt = "\sigma_v = \sqrt{\tfrac{1}{2}[(\sigma_{11} - \sigma_{22})^2 + (\sigma_{22} - \sigma_{33})^2 + (\sigma_{33} - \sigma_{11})^2 + 6(\sigma_{12}^2 + \sigma_{23}^2 + \sigma_{31}^2)]}"

    def compute_stress_trial(self, strain_increment, gp):
        D = self.linear_material.give_stiffness_matrix_plane_strain(gp)
        stress_trial = D.dot(strain_increment)
        return stress_trial


class J2PlasticityMaterialStatus(MaterialStatus):

    def __init__(self):
        super(J2PlasticityMaterialStatus, self).__init__()
