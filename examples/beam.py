"""
An example showing bending of a beam by applying a force to the end.
"""

from lolFem.core.boundary_conditions.point_load import PointLoad
from lolFem.core.boundary_conditions.dirichlet import Dirichlet
from lolFem.core.read_abaqus_mesh import read_abaqus_mesh
from lolFem.core.solvers.numpy_linalg_sp_solve import NumpyLinalgSpSolve
from lolFem.core.solvers.newton_raphson import Newton
from lolFem.core.domain import Domain
from lolFem.materials.linear_isotropic import LinearIsotropic
from lolFem.core.models.linear_static import LinearStatic
from lolFem.core.models.non_linear_static import NonLinearStatic
from lolFem.core.section import Section
from lolFem.core.dof import D_u, D_v

import numpy as np
import os

# Read in the mesh generated from Abaqus.
# This specific mesh consists of a beam, meshed with quadraterial
# elements. There are one element set called "all" which contains
# all elements. There are two node sets, one called "clamp" which
# is the nodes on the left edge and one called "force" which
# are the nodes on the right edge.
mesh = read_abaqus_mesh(os.path.abspath("meshes/beam.inp"))


# We first create a material. This is a linear isotropic material
# which is described by two parameters, E and nu.
E = 250e9
nu = 0.3
material = LinearIsotropic(E, nu)

# We then create a section. A section is a partition of the mesh
# and it is applied to the model by a method that takes a element set.
# We also give it a thickness which is used in for example plain strain
# analysis.
thickness = 1.0
section = Section(material, thickness)
# Assign section to all elements
section.assign_to(mesh, mesh.element_sets["all"])


# Boundary conditions are applied to sets of a type that fits the bc.
# Here, a dirichlet bc is applied to one node set and
# a point load is applied to another. The type of degrees
# of freedom that the boundary conditions affect is also given.
# D_u represents the spatial degree of freedom in the x-direction
# and D_v is the same but for the y-direction.
dirich = Dirichlet(0.0, [D_u, D_v], mesh.node_sets["clamp"])
dirich_2 = Dirichlet("-sin(2*pi*t)", [D_v], mesh.node_sets["force"])

# Add the boundary conditions to a "boundary condition list"
bcs = [dirich, dirich_2]


# Creates a domain. A domain consists of a mesh, a list of boundary condition
# and what type of domain it is. Here we use plain strain.
domain_type = "plane_strain"
domain = Domain(mesh, bcs, domain_type)

# Creates a solver. This is what will be used to solve for equilibrium
# in each time step. Here we use a Newton Raphson solver
rel_tol = 10e-6
miter = 10
solver = Newton(rel_tol, miter)

# Now we create a vector consisting of time points that the model
# should be run over.
timer = np.linspace(0, 1.0, 25)

print timer
# Creates a model from the solver, domain and timer and sets a
# file name to export the results to in VTK-format. This
# requires the VTK python package.
vtk_name = "results/beamo"
model = NonLinearStatic(solver, domain, timer, vtk_name)

# Starts the analysis
model.go()

print model.domain.get_all_dof_values()
