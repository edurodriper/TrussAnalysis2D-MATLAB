#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

from truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from truss_analysis_2d import Dofs, Analysis
from truss_solution import Solution, write_results
from truss_plotter import TrussPlotter


pp_project_dir = pathlib.Path('exam2024-01')
pp_project_dir = pathlib.Path('../examples/example_101')
FNAME_PREFIX = 'test'
#%%

info = Info(project_directory=str(pp_project_dir.absolute()), file_name=FNAME_PREFIX)

fileData = FileData.from_directory(info.project_directory)
mesh = Mesh()
mesh.process_mesh(file_data= fileData.mesh)

displacements = Displacements()
displacements.process_displacements(file_data= fileData.displacements)

forces = Forces()
forces.process_forces(file_data= fileData.forces)
write_input_data(info=info, mesh=mesh, displacements=displacements, forces=forces)

dofs = Dofs()
dofs.process_dofs(mesh=mesh, displacements=displacements)
analysis = Analysis()
analysis.get_global_stiffness_matrix(mesh=mesh)
analysis.get_global_force_vector(forces=forces, dofs=dofs)
analysis.get_new_displacement_vector(displacements=displacements, dofs=dofs)
analysis.get_new_transformation_matrix(displacements=displacements, dofs=dofs)  
#%%
#================== Solution ==================
solution = Solution()
solution.solve_displacement(analysis, dofs)
solution.solve_reaction(displacements=displacements)
solution.solve_stress(mesh=mesh)
# Usage example
# Assume info, mesh, displacements, and solution are instances of their respective classes with attributes set
write_results(info, mesh=mesh, displacements=displacements, solution=solution)

# %%
tp = TrussPlotter()
tp.get_plot_parameters(mesh=mesh, solution=solution)

# Usage example
# Assume info, plot, mesh, forces, and displacements are instances of their respective classes with attributes set
tp.plot_truss(info,  mesh, forces, displacements, save=True, show=True)

# %%
