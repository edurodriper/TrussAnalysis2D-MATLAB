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
pp_project_dir = pathlib.Path('../examples/example_101')
FNAME_PREFIX = 'test'


info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)

fileData = FileData.from_directory(info.project_directory)
mesh = Mesh()
mesh.process_mesh(file_data= fileData.mesh)

displacements = Displacements()
displacements.process_displacements(file_data= fileData.displacements)
forces = Forces()
forces.process_forces(file_data= fileData.forces)
#%%
truss_problem = TrussAnalysisProject(info=info, mesh=mesh, displacements=displacements, forces=forces)
truss_problem.write_input_data()
truss_problem.solve()
truss_problem.plot_truss(save=True, show=True)
# %%
