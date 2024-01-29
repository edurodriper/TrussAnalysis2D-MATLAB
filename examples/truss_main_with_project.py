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

pp_project_dir = pathlib.Path('exam2024-01')
# pp_project_dir = pathlib.Path('../examples/example_101')
FNAME_PREFIX = 'test'


info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)

fileData = FileData.from_directory(info.project_directory)
mesh = Mesh()
mesh.process_mesh(file_data= fileData.mesh)

displacements = Displacements()
displacements.process_displacements(file_data= fileData.displacements)
forces = Forces()
forces.process_forces(file_data= fileData.forces)
truss_problem = TrussAnalysisProject(info=info, mesh=mesh, displacements=displacements, forces=forces)

#%%
forces.force_components[0] = (80000,0)
#%%

truss_problem.write_input_data()
truss_problem.solve()
# truss_problem.plot_truss(save=True, show=True)
# %%
# %%
truss_problem.report_reactions(fmt='>12.1f')
truss_problem.report_rod_forces(fmt='>12.1f')

# %%


json_data ="""{
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

m_j = Mesh() 
# %%
m_j.process_mesh_json(json_data=json_data)
# %%
import json
data = json.loads(json_data)
# %%
data['nodes']
# %%
