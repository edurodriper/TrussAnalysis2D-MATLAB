#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

from truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from truss_analysis_2d import Dofs, Analysis
from truss_solution import Solution, write_results


class TrussPlotter:
    def __init__(self):
        self.plot_x_limits = None
        self.plot_y_limits = None
        self.paper_size = None
        self.paper_position = None
        self.plot_scale = None
        self.scale_factor = None

    def get_plot_parameters(self, mesh, solution):
        node_coordinates = np.array(mesh.node_coordinates)
        node_displacements = np.array(solution.global_displacements)

        # Node coordinates
        nc_x = node_coordinates[:, 0]
        nc_y = node_coordinates[:, 1]

        # Truss limits
        tx_min = np.min(nc_x)
        tx_max = np.max(nc_x)
        ty_min = np.min(nc_y)
        ty_max = np.max(nc_y)

        # Truss size
        tx_size = tx_max - tx_min
        ty_size = ty_max - ty_min

        # Margins
        margins = 0.09 * max(tx_size, ty_size)

        # Plot limits
        px_min = tx_min - margins
        px_max = tx_max + margins
        py_min = ty_min - margins
        py_max = ty_max + margins
        plot_x_limits = [px_min, px_max]
        plot_y_limits = [py_min, py_max]

        # Axis size
        ax_size = px_max - px_min
        ay_size = py_max - py_min
        
        # Figure size
        fXSize = ax_size / 0.84;
        fYSize = ay_size / 0.88;

        # Figure size and paper orientation
        if fXSize  > fYSize:
            paper_size = [29.7, 21.0]  # A4 landscape
            if fXSize / fYSize > 297 / 210:
                plot_scale = 29.7 / fXSize
            else:
                plot_scale = 21.0 / fYSize
        else:
            paper_size = [21.0, 29.7]  # A4 portrait
            if fXSize / fYSize > 210 / 297:
                plot_scale = 21.0 / fXSize
            else:
                plot_scale = 29.7 / fYSize
        paper_position = [0, 0] + paper_size

        # Deformed scale factor
        max_displ = np.max(np.abs(node_displacements))
        scale_factor = margins * 0.5 / max_displ if max_displ != 0 else 0

        self.plot_x_limits = plot_x_limits
        self.plot_y_limits = plot_y_limits
        self.paper_size = paper_size
        self.paper_position = paper_position
        self.plot_scale = plot_scale
        self.scale_factor = scale_factor

#%%

if __name__ == '__main__':
    pp_project_dir = pathlib.Path('example-np')
    info = Info(project_directory=str(pp_project_dir.absolute()), file_name='test')

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
    #================== Solution ==================
    solution = Solution()
    solution.solve_displacement(analysis, dofs)
    solution.solve_reaction(displacements=displacements)
    solution.solve_stress(mesh=mesh)
    # Usage example
    # Assume info, mesh, displacements, and solution are instances of their respective classes with attributes set
    # write_results(info, mesh=mesh, displacements=displacements, solution=solution)

    # %%
    tp = TrussPlotter()
    tp.get_plot_parameters(mesh=mesh, solution=solution)
# %%
