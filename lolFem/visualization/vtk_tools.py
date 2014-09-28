import logging

import vtk

logger = logging.getLogger(__name__)


def create_vtk_object(mesh):

    n_nodes = len(mesh.nodes)

    # Add points to vtkPoints
    points = vtk.vtkPoints()
    for node in mesh.nodes.values():
        d_coords = node.coordinates
        # TODO: fix this
        points.InsertNextPoint(d_coords + [0])

    # Add elements to vtkCellArray
    elems_vtk = vtk.vtkCellArray()
    for element in mesh.elements.values():
        elem_vtk = element.vtk_class
        for i, vertex in enumerate(element.vertices):
            elem_vtk.GetPointIds().SetId(i, vertex - 1)
        elems_vtk.InsertNextCell(elem_vtk)

    # Add tensors
    stress_array = vtk.vtkDoubleArray()
    stress_array.SetNumberOfComponents(9)
    stress_array.SetName("Stress")
    stress_array.SetNumberOfTuples(n_nodes)

    strain_array = vtk.vtkDoubleArray()
    strain_array.SetNumberOfComponents(9)
    strain_array.SetName("Strain")
    strain_array.SetNumberOfTuples(n_nodes)

    for i, node in enumerate(mesh.nodes.values()):
        # TODO: Remove hardcoded 2d plain strain

        stress = node.stress
        stress_tuple = [stress[0], stress[3], 0,
                        stress[3], stress[1], 0,
                        0, 0, stress[2]]
        stress_array.SetTuple9(i, *stress_tuple)

        node.stress_vec = []

        strain = node.strain

        strain_tuple = [strain[0], strain[3], 0,
                        strain[3], strain[1], 0,
                        0, 0, strain[2]]
        strain_array.SetTuple9(i, *strain_tuple)

        node.strain_vec = []

    # Add displacements
    disp_array = vtk.vtkDoubleArray()
    disp_array.SetNumberOfComponents(3)
    disp_array.SetName("Displacement")
    disp_array.SetNumberOfTuples(n_nodes)
    for i, node in enumerate(mesh.nodes.values()):
        # TODO: Remove hardcoding, should make like a
        # get displacements in node class
        disp = [node.dofs[0].value, node.dofs[1].value, 0]
        disp_array.SetTuple3(i, *disp)



    # Create a polydata to store everything in
    polydata = vtk.vtkPolyData()

    # Add the points to the polydata object
    polydata.SetPoints(points)

    # Add the elements to the polydata object
    polydata.SetPolys(elems_vtk)

    # Add the tensors to the data set
    polydata.GetPointData().AddArray(stress_array)
    polydata.GetPointData().AddArray(strain_array)
    polydata.GetPointData().AddArray(disp_array)

    return polydata


def write_vtk_file(mesh, name):

    polydata = create_vtk_object(mesh)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(name + str(".vtp"))
    if vtk.VTK_MAJOR_VERSION <= 5:
        writer.SetInput(polydata)
    else:
        writer.SetInputData(polydata)
    #writer.SetDataModeToAscii()
    writer.Write()


def show_data(polydata):
    # Setup actor and mapper
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polydata)
    else:
        mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Setup render window, renderer, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderer.AddActor(actor)
    renderWindow.Render()
    renderWindowInteractor.Start()
