import pytest
import numpy as np
from truss_input import Mesh, Displacements, Forces
from truss_analysis_2d import Dofs, Analysis
from truss_solution import Solution, TrussPlotter


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



def test_truss_plotter_config(mesh_inst, displ, forces):
    """Transformation matrix test

    """    
    dofs = Dofs()
    dofs.process_dofs(mesh=mesh_inst, displacements=displ)

    analysis = Analysis()
    analysis.get_global_stiffness_matrix(mesh=mesh_inst)
    analysis.get_global_force_vector(forces=forces, dofs=dofs)
    analysis.get_new_displacement_vector(displacements=displ, dofs=dofs)
    analysis.get_new_transformation_matrix(displacements=displ, dofs=dofs) 
    solution = Solution()
    # Assume analysis and dofs are instances of their respective classes with attributes set
    solution.solve_displacement(analysis, dofs)
    solution.solve_reaction( displacements= displ) 
    solution.solve_stress(mesh = mesh_inst)

    tp = TrussPlotter()
    tp.get_plot_parameters(mesh=mesh_inst,solution=solution)
    exp_scale_factor = 2.2459e+05
    assert tp.scale_factor == pytest.approx(exp_scale_factor, rel=1e-4)

    np.testing.assert_allclose(tp.paper_position, [ 0,  0,   29.7000,   21.0000])    
    np.testing.assert_allclose(tp.paper_size, [  29.7000,   21.0000])    
    
    assert tp.plot_scale == pytest.approx(3.9153, rel=1e-4)
    np.testing.assert_allclose(tp.plot_x_limits, [-0.3600,   4.3600])
    np.testing.assert_allclose(tp.plot_y_limits, [-0.3600,   4.3600])