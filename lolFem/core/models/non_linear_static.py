import logging

import numpy as np
import time
import datetime

from lolFem.core.models.model import Model

logger = logging.getLogger(__name__)

import pylab as pl


class NonLinearStatic(Model):

    def __init__(self, solver, domain, timer, vtk_file_name=None):
        super(
            NonLinearStatic,
            self).__init__(solver,
                           domain,
                           timer,
                           vtk_file_name)

    def solve(self, model):
        print "Starting solver for NonLinearStatic model..."
        start_t = time.time()

        for i, t in enumerate(self.timer):
            print "\tSolving for time: {}".format(t)
            self.solver.solve(self, t)

            # Update components
            self.update()

            if not (self.vtk_file_name is None):
                self.export_to_vtk(self.vtk_file_name + "_" + str(i))

        print "NonLinearStatic model completed in {}!".format(time.strftime('%H:%M:%S', time.gmtime(time.time() - start_t)))
