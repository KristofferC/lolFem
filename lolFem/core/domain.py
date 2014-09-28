"""
File that contains the class definition of a domain
"""

from collections import defaultdict, OrderedDict
import logging

import numpy as np
from scipy import sparse

from lolFem.core.boundary_conditions.point_load import PointLoad
from lolFem.core.dof import Dof, DT_active, DT_master


logger = logging.getLogger(__name__)


class Domain(object):

    """
    A domain holds the geometry of the model and the
    boundary conditions being applied.

    A domain contains of a mesh that contains nodes, elements and
    sets. It also holds the boundary conditions that are
    applied to the dofs living in the nodes. It has a type
    to describe the geometrical assumptions being made
    (for example "plane_strain".).
    """

    def __init__(self,
                 mesh,
                 boundary_conditions=None,
                 domain_type=None):
        """
        Initiates a domain class.

        Parameters
        ==========

        mesh: lolFem.core.mesh.Mesh
            A mesh.
        boundary_conditions: list
            List of different boundary conditions.
        domain_type: {"plane_strain"}
            Type of domain, right now, only plane strain supported

        Raises
        ======
        DomainTypeError
            If the domain type given is not supported.
        """

        self.mesh = mesh

        # Boundary conditions
        if boundary_conditions is None:
            boundary_conditions = OrderedDict()
        self.boundary_conditions = boundary_conditions

        if domain_type not in ["plane_strain"]:
            raise DomainTypeError(
                "Domain type: {} not supported").format(domain_type)
        self.domain_type = domain_type

        self.dof_bc = None
        self.number_of_equations = 0
        self.number_of_prescribed_equations = 0
        self.model = None
        self.eq_n_map = None
        self.pres_eq_n_map = None

        # Assign itself to elements
        # TODO: is this needed?
        for element in self.mesh.elements.values():
            element.domain = self

    def create_material_statuses(self):
        """
        Loops over elements and calls their own
        `create_material_statuses` methods.
        """
        for element in self.mesh.elements.values():
            element.create_material_statuses()

    def create_dofs(self):
        """
        Creates the required dofs.

        Goes through all the elements and boundary conditions
        and initiates the dofs for all the nodes. The dof type is
        determined from what type of boundary condition is applied
        to the dof.

        This also sets a class variable "dof_bc". This is a list of
        dictionaries, where each dictionary contain a mapping
        between the id of the dof and the boundary condition applied
        to it. If you for example want to see the boundary condition
        for node 3, and dof it 2, you do dof_bc[3][2}. This will
        return the boundary condition class instance active for
        that dof
        """

        # Loop over elements, lookup what dof ids the element
        # use, add this to a dictionary of such that node_dofs[node_number}
        # returns a set of the dof ids for that node.
        node_dofs = defaultdict(set)
        for element_id in self.mesh.elements:
            element = self.mesh.elements[element_id]
            for vert in element.vertices:
                node = self.mesh.nodes[vert]
                # Check what type of dofs we have in the element for the
                # current node
                dof_ids = element.give_dof_mask()

                # Add the dof types to the set at the position of the node
                # number
                [node_dofs[node.n].add(dof_id) for dof_id in dof_ids]

        logger.debug("Created the following node, dof mapping: %s", node_dofs)

        # Loop over the boundary conditions, and for each node the boundary
        # condition is applied to we add the dof of the node the bc
        # is applied to and store it.
        self.dof_bc = defaultdict(dict)
        for bc in self.boundary_conditions:
            node_ids = bc.set_applied_to.give_node_ids()

            for node_id in node_ids:
                node = self.mesh.nodes[node_id]
                node_number = node.n

                for dof_id in bc.dof_ids:
                    self.dof_bc[node_number].update({dof_id: bc})

        logger.debug(
            "Created the following node, dofid -> bc mapping: %s",
            self.dof_bc)

        # This creates instances of the dof class and append
        # them to the nodes. The type of dof is determined.
        n = 1
        for node in self.mesh.nodes.values():
            for dof_id in node_dofs[node.n]:

                # Check if the dof id of that node has a bc attached to it
                # and if that bc requires active dof
                bc = self.dof_bc[node.n].get(dof_id, 0)

                # Set the dof type according to what type of bc is acting
                if bc and bc.essential:
                    dof_type = DT_active
                else:
                    dof_type = DT_master
                node.dofs.append(Dof(n, node, dof_type, dof_id))
                n += 1

    def update_dof_values(self, u, time):
        """
        Updates dof with new values.

        This is used to propagate new  updated unknowns in for example
        a Newton Raphson step up to the dofs.

        Parameters
        ==========

        u: list of floats
            List of unknowns in order of their equation number.
        time: float
            Current time in the analysis.
        """

        for node_id, node in self.mesh.nodes.iteritems():
            # Loop over the dof ids in the node
            for dof in node.dofs:
                dof_id = dof.dof_id
                # If boundary condition, get value from
                # boundary condition class, else use
                # the value form the argument u.
                bc = self.dof_bc[node.n].get(dof_id, 0)
                if bc and bc.essential:
                    dof.value = bc.give_value(time, node)
                else:
                    dof.value += u[dof.equation_number - 1]

    def set_dof_numbering(self):
        """
        Gives all the dofs an equation number.

        If the dof does not have an essential boundary condition
        the dof is given a positive unique "equation number".
        Else it is given a negative unique "prescribed equation number".
        """

        self.number_of_equations = 0
        self.number_of_prescribed_equations = 0
        prescribed_eq_number = 1
        equation_number = 1

        # Loop over dofs in nodes and check dof type,
        # Give the dof an equation number according to this
        # type.

        # Create maps
        # Todo: document this
        eq_n_map = []
        pres_eq_n_map = []

        # Loop over dofs in nodes and check dof type,
        # Give the dof an equation number according to this
        # type.
        for node_id, node in self.mesh.nodes.iteritems():
            for dof in node.dofs:
                if dof.dof_type == DT_master:
                    dof.equation_number = equation_number
                    equation_number += 1
                    self.number_of_equations += 1
                    eq_n_map.append(dof.n)
                if dof.dof_type == DT_active:
                    dof.equation_number = -prescribed_eq_number
                    prescribed_eq_number += 1
                    self.number_of_prescribed_equations += 1
                    pres_eq_n_map.append(dof.n)

        self.eq_n_map = eq_n_map
        self.pres_eq_n_map = pres_eq_n_map

    def compute_load_vector(self, t):
        """
        Computes external load from boundary conditions.

        Loops over the dofs in the nodes and checks if a load
        is applied to that dof. In that case add it to the
        load list "f" at the position of its equation number.
        Since loads can vary with time we send in the current time
        of the analysis in the method.

        Parameters
        ==========
        time : float
            Current time in the analysis.

        Returns
        =======
        list of floats
            The external forces ordered according to their
            equation number
        """
        f = np.zeros(self.number_of_equations, dtype=np.float64)
        f_squared = np.zeros(self.number_of_equations, dtype=np.float64)
        for node_id, node in self.mesh.nodes.iteritems():
            for dof in node.dofs:
                # Check if bc is applied to the dof and that is is a load.
                bc = self.dof_bc[node.n].get(dof.dof_id, 0)
                # TODO: Fix this for more general forces
                if bc and isinstance(bc, PointLoad):
                    f[dof.equation_number - 1] = bc.give_value(t, node)
                    f_squared[dof.equation_number - 1] = bc.give_value(t, node) ** 2
        return f, f_squared

    def assemble_stiffness_matrix(self):
        """
        Assembles the global stiffness matrix.

        Loops over the elements and collect the element
        stiffness matrices. These are then assembled
        into a global stiffness matrix. Only dofs that
        do not have essential boundary conditions
        prescribed are includes into the matrix.

        The global stiffness matrix is first stored in COO-format[1]
        and is then converted to CSR-format [2] to enable
        numerical operations.

        Returns
        =======
        matrix in numpys CSR-format
            The global stiffness matrix.

        References
        ==========
        .. [1] http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html
        .. [2] http://en.wikipedia.org/wiki/Sparse_matrix#Compressed_row_Storage_.28CRS_or_CSR.29
        """

        I, J, V = [], [], []
        # Loop elements and get their element stiffness matrix Ke.
        for element in self.mesh.elements.values():
            Ke = element.compute_stiffness_matrix(self.mesh)
            dofs = []
            # Extract all dofs from the element
            for el_vert in element.vertices:
                node = self.mesh.nodes[el_vert]
                for dof in node.dofs:
                    dofs.append(dof)

            # Loop over the dofs, check if they are included in the
            # reduced equation system, and in that case, add the
            # stiffness element to the correct place in the global
            # stiffness matrix
            for i, dof_1 in enumerate(dofs):
                for j, dof_2 in enumerate(dofs):
                    if dof_1.equation_number > 0 and dof_2.equation_number > 0:
                        I.append(dof_1.equation_number - 1)
                        J.append(dof_2.equation_number - 1)
                        V.append(Ke[i, j])

        # Create COO-format matrix and convert to CSR.
        K = sparse.coo_matrix((V, (I, J)), shape=(
            self.number_of_equations, self.number_of_equations)).tocsr()
        return K

    def get_all_dof_values(self):
        """
        Gets all the values of the dofs.

        Returns
        =======
        list of floats
            values of the unknown according to their number
        """
        u = np.zeros(
            self.number_of_equations +
            self.number_of_prescribed_equations,
            dtype=np.float64)
        for node_id, node in self.mesh.nodes.iteritems():
            for dof in node.dofs:
                u[dof.n - 1] = dof.value
        return u

    def assemble_internal_forces(self, t):
        f_int, f_int_squared = self.get_internal_forces(t)
        # TODO: Fix this explicit conversion
        eq_vec = np.array(self.eq_n_map)
        return f_int[eq_vec - 1], f_int_squared[eq_vec - 1]

    def get_internal_forces(self, t):
        """
        Assembles the internal force vector.

        Sums up the contribution of the internal forces
        from all elements into a global internal force
        vector.

        This is done by calling each element to return their
        element internal force vector and the forces from each
        degree of freedom is added up. Only dofs without
        essential boundary conditions are assembled.

        Parameters
        ==========
        t : float
            The current time in the analysis

        Returns
        =======
        list of floats
            Internal forces for each dof
        """
        f_int = np.zeros(self.number_of_equations +
                          self.number_of_prescribed_equations,
                         dtype=np.float64)
        f_int_squared = np.zeros(self.number_of_equations +
                          self.number_of_prescribed_equations,
                         dtype=np.float64)
        for element_id, element in self.mesh.elements.iteritems():
            # Get the internal force for that element
            f_int_ele = element.compute_internal_forces(t)
            i = 0
            for el_vert in element.vertices:
                node = self.mesh.nodes[el_vert]
                for dof in node.dofs:
                    f_int[dof.n - 1] += f_int_ele[i]
                    f_int_squared[dof.n - 1] += f_int_ele[i] ** 2
                    i += 1
        #self.f = f_int
        #self.f_squared = f_int_squared
        return f_int, f_int_squared

    def recover_fields_in_nodes(self):
        """
        Recover fields in nodes by assigning them the field from the
        closest gauss points.

        # TODO: Fix this for n_gps != n_vertices in element
        """
        for element in self.mesh.elements.values():
            element.recover_fields_in_nodes(self.mesh)

        # Average the fields from all contribution,
        # TODO: Maybe least square instead?
        for node in self.mesh.nodes.values():
            # print "node_stress_vec"
            # print node.stress_vec
            node.stress = np.mean(node.stress_vec, axis=0)
            # print "node.stress"
            # print node.stress
            node.strain = np.mean(node.strain_vec, axis=0)

    def update(self):
        """
        Propagates the update command to all nodes
        and elements.
        """
        for node in self.mesh.nodes.values():
            node.update()

        for element in self.mesh.elements.values():
            element.update()


class DomainTypeError(Exception):

    """
    Exception to raise when an unknown domain
    type is given to the domain initiator.
    """
    pass
