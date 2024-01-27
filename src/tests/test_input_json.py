import pytest
from npp_2d_truss_analysis.truss_input import Mesh, Displacements, Forces

@pytest.fixture
def mesh_json_data():
    return """{
    "nodes": [
      {"id": 1, "coordinates": [0, 0]},
      {"id": 2, "coordinates": [0, 2]},
      {"id": 3, "coordinates": [0, 4]},
      {"id": 4, "coordinates": [4, 4]},
      {"id": 5, "coordinates": [4, 2]}
    ],
    "elements": [
      {"id": 1, "connectivity": [4, 3], "materialId": 1},
      {"id": 2, "connectivity": [3, 2], "materialId": 1},
      {"id": 3, "connectivity": [2, 4], "materialId": 1},
      {"id": 4, "connectivity": [4, 5], "materialId": 1},
      {"id": 5, "connectivity": [5, 2], "materialId": 1},
      {"id": 6, "connectivity": [2, 1], "materialId": 1},
      {"id": 7, "connectivity": [1, 5], "materialId": 1}
    ],
    "materials": [
      {"id": 1, "youngModulus": 200000000000.0, "area": 1.0}
    ]
    }"""

@pytest.fixture
def displ_json_data():
    return """{
    "pin": [
      {"id": 1, "node":4, "angle": 0,"dx": 0, "dy":0}
    ],
    "rollers": [
      {"id": 1, "node": 1, "direction": 2, "angle": 26.5651, "dx":0}
    ]
    }"""


# @pytest.fixture
# def forces_data():
#     return  [[2.0], [5.0, -180.0, 40000.0, 0.0], [3.0, 200.0, 20000.0, 0.0]]


def test_mesh_json(mesh_json_data):
    mesh = Mesh()
    mesh.process_mesh_json(mesh_json_data)
    assert mesh.number_nodes == 5
    assert mesh.number_elements == 7
    assert mesh.node_coordinates == [(0.0, 0.0), (0.0, 2.0), (0.0, 4.0), (4.0, 4.0), (4.0, 2.0)]
    assert mesh.element_connectivity == [(4, 3), (3, 2), (2, 4), (4, 5), (5, 2), (2, 1), (1, 5)]
    assert mesh.young_modulus == [200e9, 200e9, 200e9, 200e9, 200e9, 200e9, 200e9]
    assert mesh.area == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

def test_displ_json(displ_json_data):
    displ = Displacements()
    displ.process_json(displ_json_data)
    assert displ.number_pin == 1
    assert displ.pin_nodes == [4]   
    assert displ.pin_displacements == [(0.0, 0.0)]
    assert displ.pin_angles == [0.0]
    assert displ.number_roller == 1
    assert displ.roller_nodes == [1]   
    assert displ.roller_directions == [2]
    assert displ.roller_angles == [26.5651]
    assert displ.roller_displacements == [0.0]
    assert displ.number_support == 2
    assert displ.support_nodes == [4,1]

# def test_forces(forces_data):
#     forces = Forces()
#     forces.process_forces(forces_data)
#     assert forces.number_forces == 2
#     assert forces.force_nodes == [5, 3]
#     assert forces.force_components ==  [(40000.0, 0.0), (20000.0, 0.0)]
#     assert forces.force_angles == [-180.0, 200.0]