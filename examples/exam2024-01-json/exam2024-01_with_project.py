#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

from npp_2d_truss_analysis.truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from npp_2d_truss_analysis.truss_analysis_2d import Dofs, Analysis
from npp_2d_truss_analysis.truss_solution import Solution, write_results
from npp_2d_truss_analysis.truss_plotter import TrussPlotter
from npp_2d_truss_analysis.truss_project import TrussAnalysisProject


#%%

pp_project_dir = pathlib.Path('./')
# pp_project_dir = pathlib.Path('../examples/example_101')
FNAME_PREFIX = 'test'


info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)


mesh = Mesh()
# mesh.process_mesh(file_data= fileData.mesh)
mesh_json_data ="""{
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
    {"id": 7, "connectivity": [1, 0], "materialId": 1}
  ],
  "materials": [
    {"id": 1, "youngModulus": 200000000000.0, "area": 1.0}
  ]
}"""
mesh.process_mesh_json(json_data=mesh_json_data)


displacements = Displacements()
displ_json_data ="""{
  "pin": [
    {"id": 1, "node":4, "angle": 0,"dx": 0, "dy":0}
  ],
  "rollers": [
    {"id": 1, "node": 1, "direction": 1, "angle": -63.4349, "dx":0}
  ]
}"""
displacements.process_json(json_data=displ_json_data)
# displacements.process_displacements(file_data= fileData.displacements)

force_json_data ="""{
  "forces": [
    {"id": 1, "node":5, "direction": -180,"x": 40000, "y":0},
    {"id": 2, "node":1, "direction":  200,"x": 20000, "y":0}
  ]
}"""
forces = Forces.from_json(force_json_data)

truss_problem = TrussAnalysisProject(info=info, mesh=mesh, displacements=displacements, forces=forces)

#%%
# forces.force_components[0] = (80000,0)
forces.list_forces()
#%%
forces.update_force_by_id(force_id=0, fxy=(80000,0))
#%%

truss_problem.write_input_data()
truss_problem.solve()
# truss_problem.plot_truss(save=True, show=True)
# %%
# %%
truss_problem.report_reactions(fmt='>12.1f')
truss_problem.report_rod_forces(fmt='>12.1f')

# %%



m_j = Mesh() 
# %%
m_j.process_mesh_json(json_data=json_data)
# %%
import json
data = json.loads(json_data)
# %%
data['nodes']
# %%
