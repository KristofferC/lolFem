import logging

logger = logging.getLogger(__name__)


class MaterialStatus(object):

    def __init__(self):
        self.temp_strain = None
        self.temp_stress = None

        self.strain = None
        self.stress = None

    def update(self):
        self.stress = self.temp_stress
        self.strain = self.temp_strain
