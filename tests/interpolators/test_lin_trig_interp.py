import unittest

from lolFem.interpolators.lin_trig_interp import LinTrigInterp
from lolFem.core.node import Node

# TODO: Unfinished


class Test(unittest.TestCase):

    """Unit tests for interpolator for linear triangle
    elements: LinTrigInterp."""

    def setUp(self):

        self.lin_trig_interp = LinTrigInterp()
        # Set up nodes and vertices
        node_1 = Node(1.3, 0.5, 0.0)
        node_2 = Node(1.6, 1.6, 0.0)
        node_3 = Node(0.2, 0.9, 0.0)

        self.nodes = {1: node_1, 2: node_2, 3: node_3}
        self.vertices = [1, 2, 3]

    def test_eval_N(self):
        local_coords = [0.5, 0.3, 0.0]
        N = self.lin_trig_interp.eval_N(local_coords)
        assert(N[0] == 0.5)
        assert(N[1] == 0.3)
        assert(N[2] == 1.0 - 0.5 - 0.3)

    def test_eval_dNdx(self):
        pass

    def test_give_area(self):
        assert (
            abs(self.lin_trig_interp.give_area(self.vertices, self.nodes) - 0.6650) < 10e-14)

    # def test_local_to_global(self):

        # First check local vertices transform to global vertices
        #local_coords = [0.0, 0.0, 0.0]
        # diff = self.lin_trig_interp.local_to_global(local_coords, self.vertices, self.nodes) - self.nodes[1].
        #assert np.linalg.norm(diff) < 10e-14
        #local_coords = [0.0, 1.0, 0.0]
        # print self.lin_trig_interp.local_to_global(local_coords, self.vertices, self.nodes)
        #local_coords = [1.0, 0.0, 0.0]
        # print self.lin_trig_interp.local_to_global(local_coords,
        # self.vertices, self.nodes)

    # def global_to_local:
    #     pass


if __name__ == "__main__":
    unittest.main()
