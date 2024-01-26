import pytest
import numpy as np
from truss_input import Mesh, Displacements, Forces
from truss_analysis_2d import Dofs, Analysis
from truss_solution import Solution


@pytest.fixture
def mesh_inst():
    mesh_data = [[5.0],
        [0.0, 0.0],
        [0.0, 2.0],
        [0.0, 4.0],
        [4.0, 4.0],
        [4.0, 2.0],
        [7.0],
        [4.0, 3.0, 1.0],
        [3.0, 2.0, 1.0],
        [2.0, 4.0, 1.0],
        [4.0, 5.0, 1.0],
        [5.0, 2.0, 1.0],
        [2.0, 1.0, 1.0],
        [1.0, 5.0, 1.0],
        [1.0],
        [200000000000.0, 1.0]]
    _mesh = Mesh()
    _mesh.process_mesh(mesh_data)
    return _mesh


@pytest.fixture
def displ():
    displ_data = [[1.0], [4.0, 0.0, 0.0, 0.0], [1.0], [1.0, 2.0, 26.5651, 0.0], []]
    _displ = Displacements()
    _displ.process_displacements(displ_data)
    return _displ

@pytest.fixture
def forces():
    forces_data =  [[2.0], [5.0, -180.0, 40000.0, 0.0], [3.0, 200.0, 20000.0, 0.0]]
    _forces = Forces()
    _forces.process_forces(forces_data)
    return _forces

def test_dofs(mesh_inst, displ, forces):
    dofs = Dofs()
    dofs.process_dofs(mesh=mesh_inst, displacements=displ)
    assert dofs.number_dofs == 10
    assert dofs.number_fixed == 3
    assert dofs.number_free == 7
    assert dofs.fixed_dofs ==  [7, 8, 1]
    assert dofs.free_dofs == [2, 3, 4, 5, 6, 9, 10]


def test_tm(mesh_inst, displ, forces):
    """Transformation matrix test

    """    
    dofs = Dofs()
    dofs.process_dofs(mesh=mesh_inst, displacements=displ)

    analysis = Analysis()
    # Assume mesh is an instance of the Mesh class with attributes set
    analysis.get_global_stiffness_matrix(mesh=mesh_inst)
    analysis.get_global_force_vector(forces=forces, dofs=dofs)
    analysis.get_new_displacement_vector(displacements=displ, dofs=dofs)
    analysis.get_new_transformation_matrix(displacements=displ, dofs=dofs) 

    expected = np.eye(10)
    expected[0,0] = 0.89442681
    expected[0,1] = 0.44721436
    expected[1,0] = -0.44721436
    expected[1,1] = 0.89442681
 
    np.testing.assert_allclose(expected, analysis.transformation_new_matrix, rtol=1e-5, atol=1e-5)


def test_solution_solve_displacements(mesh_inst, displ, forces):
    """Transformation matrix test

    """    
    dofs = Dofs()
    dofs.process_dofs(mesh=mesh_inst, displacements=displ)

    analysis = Analysis()
    # Assume mesh is an instance of the Mesh class with attributes set
    analysis.get_global_stiffness_matrix(mesh=mesh_inst)
    analysis.get_global_force_vector(forces=forces, dofs=dofs)
    analysis.get_new_displacement_vector(displacements=displ, dofs=dofs)
    analysis.get_new_transformation_matrix(displacements=displ, dofs=dofs) 
    solution = Solution()
    # Assume analysis and dofs are instances of their respective classes with attributes set
    solution.solve_displacement(analysis, dofs)
    
    expected =   [0, 3.2521e-07,  -5.2783e-07, 2.9088e-07, -3.7588e-07, 2.2248e-07, 0, 0,   -8.0144e-07, 1.3160e-07]

    np.testing.assert_allclose(expected, solution.new_displacements, rtol=1e-5, atol=1e-5)