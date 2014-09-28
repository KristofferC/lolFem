

from lolFem.core.boundary_conditions import PointLoad
from lolFem.core.boundary_conditions import Dirichlet
from lolFem.core.node_set import NodeSet
from lolFem.core.solvers import NumpyLinalgSpSolve
from lolFem.core.domain import Domain
from lolFem.elements.trig_plane_strain import TrigPlaneStrain
from lolFem.core.node import Node
from lolFem.core.mesh import Mesh
from lolFem.materials.linear_isotropic import LinearIsotropic
from lolFem.core.element_set import ElementSet
from lolFem.core.models.linear_static import LinearStatic
from lolFem.core.section import Section
from lolFem.core.dof import D_u, D_v

# Nodes
node_1 = Node(1, [0, 0])
node_2 = Node(2, [1, 1])
node_3 = Node(3, [1, 2])
node_4 = Node(4, [0, 1])


# Elements
element_1 = TrigPlaneStrain(1, [1, 2, 3])
element_2 = TrigPlaneStrain(2, [1, 2, 4])

# Sets
bottom_set = NodeSet("y0", [1])
top_set = NodeSet("x0", [2, 3])
node_sets = [bottom_set, top_set]

# Element set
element_set = ElementSet("all", [1, 2])

# Create mesh
mesh = Mesh()
mesh.add_node(node_1)
mesh.add_node(node_2)
mesh.add_node(node_3)
mesh.add_node(node_4)
mesh.add_element(element_1)
mesh.add_element(element_2)
mesh.add_element_set(element_set)
mesh.add_node_set(bottom_set)
mesh.add_node_set(top_set)


# Materials
material = LinearIsotropic(250e9, 0.3)

# Section to element sets
thickness = 2.0
section = Section(material, thickness)
section.assign_to(mesh, mesh.element_sets["all"])


# Boundary conditions

dirich = Dirichlet(0.0, [D_u, D_v], mesh.node_sets["x0"])
load = PointLoad(10e5, [D_v], mesh.node_sets["y0"])

bcs = [dirich, load]


# Create domain
domain_type = "plane_strain"
domain = Domain(mesh, bcs, domain_type)


solver = NumpyLinalgSpSolve()

model = LinearStatic(solver, domain)

u = model.go()

print u
