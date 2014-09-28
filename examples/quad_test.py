"""This shows a simple example of two connected quadraterials.
Here the elements, nodes and all sets are created are all
created in the file"""

from lolFem.core.boundary_conditions.point_load import PointLoad
from lolFem.core.boundary_conditions.dirichlet import Dirichlet
from lolFem.core.node_set import NodeSet
from lolFem.core.solvers.numpy_linalg_sp_solve import NumpyLinalgSpSolve
from lolFem.core.domain import Domain
from lolFem.elements.quad_plane_strain import QuadPlaneStrain
from lolFem.core.node import Node
from lolFem.core.mesh import Mesh
from lolFem.core.element_set import ElementSet
from lolFem.core.models.linear_static import LinearStatic
from lolFem.core.section import Section
from lolFem.core.dof import D_u, D_v
from lolFem.materials.linear_isotropic import LinearIsotropic


# Nodes
node_1 = Node(1, [0, 0])
node_2 = Node(2, [1, 0])
node_3 = Node(3, [0, 1])
node_4 = Node(4, [1, 1])
node_5 = Node(5, [0, 2])
node_6 = Node(6, [1, 2])


# Elements
element_1 = QuadPlaneStrain(1, [1, 2, 4, 3])
element_2 = QuadPlaneStrain(2, [3, 4, 6, 5])


# Sets
bottom_set = NodeSet("y0", [1, 2])
top_set = NodeSet("y1", [5, 6])
node_sets = [bottom_set, top_set]

# Element set
element_set = ElementSet("all", [1, 2])

# Create mesh
mesh = Mesh()
mesh.add_node(node_1)
mesh.add_node(node_2)
mesh.add_node(node_3)
mesh.add_node(node_4)
mesh.add_node(node_5)
mesh.add_node(node_6)
mesh.add_element(element_1)
mesh.add_element(element_2)
mesh.add_element_set(element_set)
mesh.add_node_set(bottom_set)
mesh.add_node_set(top_set)


# Materials
material = LinearIsotropic(250e9, 0.3)

# Section
thickness = 1.0
section = Section(material, thickness)
section.assign_to(mesh, mesh.element_sets["all"])


# Boundary conditions
dirich = Dirichlet(0.0, [D_u, D_v], mesh.node_sets["y0"])
load = PointLoad(10e8, [D_v], mesh.node_sets["y1"])

bcs = [dirich, load]


# Create domain
domain_type = "plane_strain"
domain = Domain(mesh, bcs, domain_type)

solver = NumpyLinalgSpSolve()
#solver = Newton(10e-6)
time = [1]
model = LinearStatic(solver, domain, time)
#model = NonLinearStatic(solver, domain, time)
model.go()

print model.domain.get_all_dof_values()

# print model.u

# print u
