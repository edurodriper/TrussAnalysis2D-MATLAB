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
JSON_FILE_NAME = pp_project_dir /'exam2024-01.json'
FNAME_PREFIX = 'test'


info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)

# read the JSON_FILE_NAME file content into json_problem_data string
with open(JSON_FILE_NAME, 'r') as json_file:
    json_problem_data = json_file.read()

mesh = Mesh.from_json(json_data=json_problem_data)

displacements = Displacements.from_json(json_str=json_problem_data)
# displacements.process_displacements(file_data= fileData.displacements)

forces = Forces.from_json_str(json_problem_data)
#%%
truss_problem = TrussAnalysisProject(info=info, mesh=mesh, displacements=displacements, forces=forces)

#%%
# forces.force_components[0] = (80000,0)
forces.list_forces()
#%%
forces.update_force_by_id(force_id=0, fxy=(80000,0))
#%%

truss_problem.write_input_data()
truss_problem.solve()
truss_problem.plot_truss(save=True, show=True)
# %%
# %%
truss_problem.report_reactions(fmt='>12.1f')
truss_problem.report_rod_forces(fmt='>12.1f')

# %%