import logging

import numpy as np
import time
import datetime

from lolFem.core.models.model import Model

logger = logging.getLogger(__name__)



class Static(Model):

    def __init__(self, solver, domain, time_assistant, vtk_file_name=None):
        super(
            Static,
            self).__init__(solver,
                           domain,
                           time_assistant,
                           vtk_file_name)

    def solve(self, model):
        print "Starting solver for Static model..."
        start_t = time.time()

        for i, t in enumerate(self.time_assistant.times()):
            print "\tSolving for time: {}".format(t)
            self.solver.solve(self, self.time_assistant)

            self.update()

            if not (self.vtk_file_name is None):
                self.export_to_vtk(self.vtk_file_name + "_" + str(i))

        print ("Static model completed in {}!"
               .format(time.strftime('%H:%M:%S', time.gmtime(time.time() - start_t))))
