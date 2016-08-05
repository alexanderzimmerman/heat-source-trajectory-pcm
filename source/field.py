import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import warnings
import pandas
melt_temperature = 0
space_dims = 2
nodes_per_cell = pow(2, space_dims)  # This doesn't consider hanging nodes
temperature = -1
material = {'name': 'water-ice', 'melting temperature': 0}


def solve_pde(state):
    solution_file_name = '../PDE/example_solution.vtk'
    warnings.warn("PDE solver not yet integrated; instead reading solution from "+solution_file_name)
    warnings.warn("Ignoring state "+str(state))
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    return data


def test():
    state = (0., 0., 0.)
    data = solve_pde(state)
    print(data)

if __name__ == "__main__":
    test()
