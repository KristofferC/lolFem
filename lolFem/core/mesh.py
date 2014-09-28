"File to hold the Mesh class"

from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class Mesh(object):

    """
    A class that represents a mesh.

    A mesh is a collection of elements, nodes
    and different type of sets.
    """

    def __init__(self,
                 nodes=None,
                 elements=None,
                 element_sets=None,
                 node_sets=None):
        """

        Parameters
        ==========
        nodes : ordered dictionary
            The nodes in the mesh. The dictionary should have
            the format {node identifier (int) : `Node`}
        elements : ordered dictionary
            The elements in the mesh. The dictionary should have
            the format {element identifier (int) : `Element`}
        element_sets : ordered dictionary
             The element sets in the mesh. The dictionary should have
            the format {element set name (string) : List of element identifiers (int)}
        node_sets : ordered dictionary
            The node sets in the mesh. The dictionary should have
            the format {nodeset name (string) : List of node identifiers (int)}

        """

        # Nodes
        if nodes is None:
            nodes = OrderedDict()
        self.nodes = nodes

        # Element list
        if elements is None:
            elements = OrderedDict()
        self.elements = elements

        # Element sets
        if element_sets is None:
            element_sets = OrderedDict()
        self.element_sets = element_sets

        # Node sets
        if node_sets is None:
            node_sets = OrderedDict()
        self.node_sets = node_sets

    def add_node(self, node):
        """
        Adds a node to the mesh.
        """
        self.nodes[node.n] = node

    def add_element(self, element):
        """
        Adds an element to the mesh.
        """
        self.elements[element.n] = element

    def add_element_set(self, element_set):
        """
        Adds an element set to the mesh.
        """
        self.element_sets[element_set.name] = element_set

    def add_node_set(self, node_set):
        """
        Adds a node set to the mesh.
        """
        self.node_sets[node_set.name] = node_set
