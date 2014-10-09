"""
An example showing bending of a beam by applying a force to the end.
"""
import os


from lolFem.core.boundary_conditions.dirichlet import Dirichlet
from lolFem.core.read_abaqus_mesh import read_abaqus_mesh
from lolFem.core.solvers.newton_raphson import Newton
from lolFem.core.domain import Domain
from lolFem.materials.linear_isotropic import LinearIsotropic
from lolFem.core.models.static import Static
from lolFem.core.section import Section
from lolFem.core.dof import D_u, D_v


mesh = read_abaqus_mesh(os.path.abspath("meshes/square_with_circles_fine.inp"))


# Two different materials, one hard one soft
E_1 = 100e9
nu_1 = 0.45
material_hard = LinearIsotropic(E_1, nu_1)

E_2 = 10e9
nu_2 = 0.3
material_soft = LinearIsotropic(E_2, nu_2)


# Two sections, one for each material, assign them to different parts
thickness = 1.0
section_hard = Section(material_hard, thickness)
section_soft = Section(material_soft, thickness)
section_hard.assign_to(mesh, mesh.element_sets["Circ"])
section_soft.assign_to(mesh, mesh.element_sets["matrix"])

# BCs
dirich_1 = Dirichlet("y*t", [D_v], mesh.node_sets["edges"])
dirich_5 = Dirichlet(0.0, [D_u], mesh.node_sets["edges"])

# Add the boundary conditions to a "boundary condition list"
bcs = [dirich_1, dirich_5]


# Plane strain domain
domain_type = "plane_strain"
domain = Domain(mesh, bcs, domain_type)

# Newton Raphson solver
rel_tol = 10e-3
miter = 10
solver = Newton(rel_tol, miter)

# Only one time.
timer = [0.5]

# Make model
vtk_name = "results/homogen_y"
model = Static(solver, domain, timer, vtk_name)

# Start 'er up.
model.go()

print model.domain.get_all_dof_values()

