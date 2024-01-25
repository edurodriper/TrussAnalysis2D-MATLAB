import pytest
from truss_input import Mesh, Displacements, Forces
from truss_analysis_2d import Dofs

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
