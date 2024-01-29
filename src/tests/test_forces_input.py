import pytest
from npp_2d_truss_analysis.truss_input import Mesh, Displacements, Forces

@pytest.fixture
def forces_json_data():
    return  """{
  "forces": [
    {"id": 1, "node":5, "direction": -180,"x": 40000, "y":0},
    {"id": 2, "node":3, "direction":  200,"x": 20000, "y":0}
  ]
}"""

def test_forces_json(forces_json_data):
    forces = Forces()
    forces.process_json(forces_json_data)
    assert forces.number_forces == 2
    assert forces.force_nodes == [5, 3]
    assert forces.force_components ==  [(40000.0, 0.0), (20000.0, 0.0)]
    assert forces.force_angles == [-180.0, 200.0]


def test_forces_from_json(forces_json_data):
    forces = Forces.from_json_str(forces_json_data)
    assert forces.number_forces == 2
    assert forces.force_nodes == [5, 3]
    assert forces.force_components ==  [(40000.0, 0.0), (20000.0, 0.0)]
    assert forces.force_angles == [-180.0, 200.0]


def test_forces_update_force_node(forces_json_data):
    forces = Forces.from_json_str(forces_json_data)

    f0bef = forces.get_force_by_id(id=0)
    assert 0 == f0bef['id']
    assert 5 == f0bef['node']
    assert (40000.0, 0.0) == f0bef['fxy']
    assert -180 == f0bef['angle']
    # change node
    forces.update_force_by_id(force_id=0, node=4)
    f0aft = forces.get_force_by_id(id=0)
    assert 0 == f0aft['id']
    assert 4 == f0aft['node']
    assert (40000.0, 0.0) == f0aft['fxy']
    assert -180 == f0aft['angle']
    # change force componetns
    forces.update_force_by_id(force_id=0, fxy=(0, 10000))
    f0aft = forces.get_force_by_id(id=0)
    assert 0 == f0aft['id']
    assert 4 == f0aft['node']
    assert (0, 10000) == f0aft['fxy']
    assert -180 == f0aft['angle']
    # change angle componets
    forces.update_force_by_id(force_id=0, angle=160)
    f0aft = forces.get_force_by_id(id=0)
    assert 0 == f0aft['id']
    assert 4 == f0aft['node']
    assert (0, 10000) == f0aft['fxy']
    assert 160 == f0aft['angle']

def test_force_invalid_updates(forces_json_data):
    forces = Forces.from_json_str(forces_json_data)
    # invalid ID node
    with pytest.raises(ValueError):
        forces.update_force_by_id(force_id=-1, node=4)
    with pytest.raises(ValueError):
        forces.update_force_by_id(force_id=5, node=4)
    # invalid fxy
    with pytest.raises(AssertionError):
        forces.update_force_by_id(force_id=0, fxy='a')
    with pytest.raises(AssertionError):
        forces.update_force_by_id(force_id=0, fxy=('1',0))        
    with pytest.raises(AssertionError):
        forces.update_force_by_id(force_id=0, fxy=(0,1,0)) 