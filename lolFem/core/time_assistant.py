"""
File for the TimeAssistant class
"""

class TimeAssistant(object):
    """
    The TimeAssistant is passed around in the analysis and includes
    information about time.

    For example, time dependant boundary conditions need to know
    the current time and some materials need to know the time
    step from the last iteration.
    """
    def __init__(self, t_steps):
        """
        Initiates a TimeAssistant.

        t_vec: list of floats
            This is a list of the times to be used in the analysis.
        """

        # TODO: This need to be fixed up if we want to change dt
        # dynamically during a run.

        self.dt = 0
        self.t_steps = t_steps
        self.beg_time = t_steps[0]

        self.curr_time = None
        self.prev_time = 0

        # Creates a generator to loop over in iterations
        # Updates dt and other things
        def time_gen():
            for i in xrange(len(t_steps)):
                self.curr_time = t_steps[i]
                self.dt = self.curr_time - self.prev_time
                yield self.curr_time
                self.prev_time = self.curr_time


        self.times = time_gen
