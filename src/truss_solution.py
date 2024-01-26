#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

from truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from truss_analysis_2d import Dofs, Analysis

class Solution:
    def __init__(self):
        self.new_displacements = None
        self.new_forces = None
        self.global_displacements = None
        self.global_forces = None
        self.global_reactions = None
        self.element_stress = None
        self.element_force = None

    def solve_displacement(self, analysis, dofs):
        fixed_dofs = dofs.fixed_dofs
        free_dofs = dofs.free_dofs
        f = analysis.force_global_vector
        uc = analysis.displacement_new_vector
        tc = analysis.transformation_new_matrix
        k = analysis.stiffness_global_matrix

        # New force vector
        fc = tc @ f
        # New stiffness matrix
        kc = tc @ k @ tc.T

        # Free new displacements
        uc[free_dofs] = np.linalg.solve(kc[np.ix_(free_dofs, free_dofs)], 
                                        fc[free_dofs] - kc[np.ix_(free_dofs, fixed_dofs)] @ uc[fixed_dofs])

        # Fixed new forces
        fc[fixed_dofs] = kc[np.ix_(fixed_dofs, free_dofs)] @ uc[free_dofs] + \
                         kc[np.ix_(fixed_dofs, fixed_dofs)] @ uc[fixed_dofs] - fc[fixed_dofs]

        # Global displacement and force vectors
        u = tc.T @ uc
        f = tc.T @ fc

        self.new_displacements = uc
        self.new_forces = fc
        self.global_displacements = u
        self.global_forces = f

class Plot:
    def __init__(self):
        self.plot_x_limits = None
        self.plot_y_limits = None
        self.paper_size = None
        self.paper_position = None
        self.scale_factor = None

#%%

if __name__ == '__main__':
    pp_project_dir = pathlib.Path('example-np')
    info = Info(project_directory=str(pp_project_dir.absolute()), file_name='test')
    # %%
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
    solution = Solution()
    # Assume analysis and dofs are instances of their respective classes with attributes set
    solution.solve_displacement(analysis, dofs)
    print("Displacements==============================")
    print(solution.new_displacements)
    print(solution.new_displacements.shape)
    print(solution.new_displacements.dtype)

    # %%
