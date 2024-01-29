#%%[markdown]
# # Scope 
# This is a version of the trust analysis project that uses the class analysis class with the class method from Json file.
# The main difference from the world other version is that individual mesh displacements and forces objects are not created.
# 
# # Notes
# Additionally in this example I am adding the update methods suitable for marking my exam. 
# So please disregard any code snippets that have the `am` variable inside
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
FNAME_PREFIX = 'test'

info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)

JSON_TEXT="""{
    "mesh":{
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
    },
    "displacements":{
        "pin": [
        {"id": 1, "node":4, "angle": 0,"dx": 0, "dy":0}
        ],
        "rollers": [
        {"id": 1, "node": 1, "direction": 1, "angle": -63.4349, "dx":0}
        ]
    },
    "forces": [
      {"id": 1, "node":5, "direction": -180,"x": 40000, "y":0},
      {"id": 2, "node":3, "direction":  200,"x": 20000, "y":0}
    ]
}"""


truss_problem = TrussAnalysisProject.from_json(json_text=JSON_TEXT, info=info)

#%%
# truss_problem._forces.list_forces()
#%%
am = 20413 
xy =am%100
truss_problem._forces.update_force_by_id(force_id=1, angle=180+20+xy)
#%%
truss_problem._forces.list_forces()
#%%
truss_problem.write_input_data()
truss_problem.solve()
# truss_problem.plot_truss(save=True, show=True)
print("-------------solution ----------------")
truss_problem.report_reactions(fmt='>12.1f')
truss_problem.report_rod_forces(fmt='>12.1f')

# %%
truss_problem.plot_deformation(save=True, show=True)
truss_problem.plot_stresses(save=True, show=True)
# %%
