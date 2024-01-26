#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt

from truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from truss_analysis_2d import Dofs, Analysis
from truss_solution import Solution, write_results


def get_roller_lines(app_point, dir_vector, plot_scale):
    """returns the 

    Args:
        app_point (list two elemetns): list element
        dir_vector (int): 1-normal, 2-parallel
        plot_scale (float): plot scale

    Returns:
        list: [x1,y1, x2,y2] end coordinates of roller
    """    
    roller_l_paper = 16  # mm
    roller_h_paper = 2.5  # mm

    roller_l = roller_l_paper / 10 / plot_scale  # converting to meters
    roller_h = roller_h_paper / 10 / plot_scale  # converting to meters

    d_dir = dir_vector
    n_dir = np.array([[0, -1], [1, 0]]) @ d_dir

    point_o = app_point
    point_a1 = point_o + (n_dir * roller_h / 2) - (d_dir * roller_l / 2)
    point_b1 = point_o + (n_dir * roller_h / 2) + (d_dir * roller_l / 2)
    point_a2 = point_o - (n_dir * roller_h / 2) - (d_dir * roller_l / 2)
    point_b2 = point_o - (n_dir * roller_h / 2) + (d_dir * roller_l / 2)

    draw_seg = np.array([point_a1, point_b1, point_a2, point_b2])
    return draw_seg


def get_force_arrow(app_point, dir_vector, vector_length, plot_scale):
    arrow_l_paper = 3  # mm
    arrow_w_paper = 2  # mm
    vector_l_paper = vector_length  # mm

    arrow_l = arrow_l_paper / 10 / plot_scale  # converting to meters
    arrow_w = arrow_w_paper / 10 / plot_scale  # converting to meters
    vector_l = vector_l_paper / 10 / plot_scale  # converting to meters

    d_dir = dir_vector
    n_dir = np.array([[0, -1], [1, 0]]) @ d_dir

    point_o = app_point
    point_c = point_o + d_dir * vector_l
    point_a = point_c - (d_dir * arrow_l) + (n_dir * arrow_w / 2)
    point_b = point_c - (d_dir * arrow_l) - (n_dir * arrow_w / 2)

    draw_seg = np.array([point_o, point_c, point_a, point_c, point_b, point_c])
    return draw_seg

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
        fXSize = ax_size / 0.84
        fYSize = ay_size / 0.88

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


    def plot_truss(self, info, mesh, forces, displacements, save:bool=True, show:bool=True):
        project_dir = info.project_directory
        file_name = info.file_name
        plot_x_limits = self.plot_x_limits
        plot_y_limits = self.plot_y_limits
        paper_size = self.paper_size
        number_nodes = mesh.number_nodes
        number_elements = mesh.number_elements
        node_coordinates = np.array(mesh.node_coordinates)
        element_connectivity = mesh.element_connectivity
        number_forces = forces.number_forces
        force_nodes = forces.force_nodes
        force_components = np.array(forces.force_components)
        force_angles = forces.force_angles
        pin_nodes = displacements.pin_nodes
        number_roller = displacements.number_roller
        roller_nodes = displacements.roller_nodes
        roller_directions = displacements.roller_directions
        roller_angles = displacements.roller_angles

        new_file_name = f"{file_name}_TRUSS.pdf"
        file_path = f"{project_dir}/{new_file_name}"

        # Node number text real displacement
        d_x_real = 0.14 / self.plot_scale  # meters
        d_y_real = 0.5 / self.plot_scale  # meters

        # Create figure and axes
        fig, ax = plt.subplots(figsize=(paper_size[0]/2.54, paper_size[1]/2.54))  # Size in inches
        ax.set_xlim(plot_x_limits)
        ax.set_ylim(plot_y_limits)
        ax.set_title(f"{file_name}: Truss")
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_aspect('equal', adjustable='box')

        # plot rollers 
        for num_rol in range(number_roller):
            r_node = roller_nodes[num_rol] - 1  # Adjust for zero-based indexing in Python
            r_direction = roller_directions[num_rol]
            r_angle = roller_angles[num_rol]
            c = np.cos(np.radians(r_angle))
            s = np.sin(np.radians(r_angle))

            r_dir_vec = np.array([c, s]) if r_direction == 1 else np.array([-s, c])

            draw_seg = get_roller_lines(node_coordinates[r_node,:], r_dir_vec, self.plot_scale)
            for seg in range(2):
                ax.plot(draw_seg[2*seg:2*seg+2, 0], draw_seg[2*seg:2*seg+2, 1],
                        linestyle='-', linewidth=1, marker='none', color='black')

        # Plot elements
        for i in range(number_elements):
            node1, node2 = element_connectivity[i]
            x_coords = [node_coordinates[node1-1][0], node_coordinates[node2-1][0]]
            y_coords = [node_coordinates[node1-1][1], node_coordinates[node2-1][1]]
            ax.plot(x_coords, y_coords, linestyle='-', linewidth=2.5, color='grey')

        # plot forces
        for num_for in range(number_forces):
            f_node = force_nodes[num_for] - 1  # Adjust for zero-based indexing in Python
            f_comp_xi_yi = force_components[num_for, :]
            f_angle = force_angles[num_for]
            c = np.cos(np.radians(f_angle))
            s = np.sin(np.radians(f_angle))
            t = np.array([[c, s], [-s, c]])
            f_comp_xy = t.T @ f_comp_xi_yi
            f_dir_vec = f_comp_xy / np.linalg.norm(f_comp_xy)

            draw_seg = get_force_arrow(node_coordinates[f_node,:], f_dir_vec, 14, self.plot_scale)
            for seg in range(3):
                ax.plot(draw_seg[2*seg:2*seg+2, 0], draw_seg[2*seg:2*seg+2, 1],
                        linestyle='-', linewidth=1.3, marker='none', color='black')


        # % Nodes
        node_x_coord = node_coordinates[:, 0]
        node_y_coord = node_coordinates[:, 1]
        ax.plot(node_x_coord, node_y_coord, linestyle='none', linewidth=1,
            marker='o', markersize=14, markeredgecolor='black', 
            markerfacecolor='white')

        # % Pin nodes
        pin_nodes_adjusted = [pn - 1 for pn in pin_nodes]

        # Pin Nodes
        pin_x_coord = node_coordinates[pin_nodes_adjusted, 0]
        pin_y_coord = node_coordinates[pin_nodes_adjusted, 1]
        ax.plot(pin_x_coord, pin_y_coord, linestyle='none', linewidth=1.5,
                marker='o', markersize=5, markeredgecolor='black',
                markerfacecolor='black')

        # Roller nodes
        roller_nodes_adjusted = [rn - 1 for rn in roller_nodes]
        # Roller Nodes
        roller_x_coord = node_coordinates[roller_nodes_adjusted, 0]
        roller_y_coord = node_coordinates[roller_nodes_adjusted, 1]
        ax.plot(roller_x_coord, roller_y_coord, linestyle='none', linewidth=1.5,
                marker='o', markersize=5, markeredgecolor='black',
                markerfacecolor='white')

        # Force nodes
        force_nodes_adjusted = [fn - 1 for fn in force_nodes]
        force_x_coord = node_coordinates[force_nodes_adjusted, 0]
        force_y_coord = node_coordinates[force_nodes_adjusted, 1]
        ax.plot(force_x_coord, force_y_coord, linestyle='none', linewidth=0.1,
                marker='o', markersize=1.3, markeredgecolor='black',
                markerfacecolor='black')

        # Plot node numbers
        for i in range(number_nodes):
            x, y = node_coordinates[i]
            ax.text(x + d_x_real, y + d_y_real, str(i+1), fontsize=6, 
                    ha='center', va='center', backgroundcolor='white')

        # Plot element numbers
        for i in range(number_elements):
            node1, node2 = element_connectivity[i]
            mid_point = (node_coordinates[node1-1] + node_coordinates[node2-1]) / 2
            ax.text(mid_point[0], mid_point[1], str(i+1), fontsize=6, 
                    ha='center', va='center', backgroundcolor='white')

        # Save plot as PDF
        if save:
            plt.savefig(file_path)
        if show:
            plt.show()
        plt.close()

    def plot_stress(self, info, mesh, forces, displacements, solution, save:bool=True, show:bool=True):
        pass
        NotImplementedError()

    def plot_deformation(self, info, mesh, forces, displacements, solution, save:bool=True, show:bool=True):
        pass
        NotImplementedError()

#%%

if __name__ == '__main__':
    # pp_project_dir = pathlib.Path('example-np')
    pp_project_dir = pathlib.Path('exam2024-01')
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
    write_results(info, mesh=mesh, displacements=displacements, solution=solution)

    # %%
    tp = TrussPlotter()
    tp.get_plot_parameters(mesh=mesh, solution=solution)

    tp.plot_truss(info,  mesh, forces, displacements, save=True, show=True)

# %%
