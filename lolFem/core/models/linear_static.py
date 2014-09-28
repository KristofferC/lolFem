"""
File containing the LinearStatic class
"""
import time
import datetime

import numpy as np

from lolFem.core.models.model import Model


class LinearStatic(Model):

    """
    Model assuming static conditions and linearity in stress vs strain.
    """

    def __init__(self, solver, domain, timer, vtk_name):
        super(LinearStatic, self).__init__(solver, domain, timer, vtk_name)

    def solve(self, model):
        """
        Solves the model for the time steps. In each time step
        the equation Ku = f is solved for u, and the relative
        residual is printed:

        ..math:: R_\text{rel} = \frac{ \sum \left| f_\text{ext} - f_\text{int} \right|}{\sum |f_\text{ext}|_2  + |f_\text{int}|_2}
        """

        print "Starting solver for LinearStatic model..."
        start_t = time.time()
        u = np.zeros(self.domain.number_of_equations, dtype=np.float64)
        for i, t in enumerate(self.timer):
            print "\tSolving for time: {}".format(t)
            self.solver.solve(self, t)
            # Update components.
            self.update()

            if not (self.vtk_file_name is None):
                self.export_to_vtk(self.vtk_file_name + "_" + str(i))

        print "LinearStatic model completed in {}!".format(time.strftime('%H:%M:%S', time.gmtime(time.time() - start_t)))
