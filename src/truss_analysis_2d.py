#%%
import tkinter as tk
from tkinter import filedialog
import csv
import pathlib
from truss_input import Info, FileData,Mesh,Displacements,Forces
import numpy as np

class Dofs:
    def __init__(self):
        self.number_dofs = None
        self.number_fixed = None
        self.number_free = None
        self.fixed_dofs = None
        self.free_dofs = None

    def process_dofs(self, mesh, displacements):
        number_nodes = mesh.number_nodes
        number_pin = displacements.number_pin
        pin_nodes = displacements.pin_nodes
        number_roller = displacements.number_roller
        roller_nodes = displacements.roller_nodes
        roller_directions = displacements.roller_directions

        number_dofs = 2 * number_nodes
        number_fixed_dofs = 2 * number_pin + number_roller
        number_free_dofs = number_dofs - number_fixed_dofs
        fixed_dofs = []

        for node in pin_nodes:
            fixed_dofs.extend([2 * node - 1, 2 * node])

        for node, direction in zip(roller_nodes, roller_directions):
            if direction == 1:
                fixed_dofs.append(2 * node)
            else:
                fixed_dofs.append(2 * node - 1)

        free_dofs = [dof for dof in range(1, number_dofs + 1) if dof not in fixed_dofs]

        self.number_dofs = number_dofs
        self.number_fixed = number_fixed_dofs
        self.number_free = number_free_dofs
        self.fixed_dofs = fixed_dofs
        self.free_dofs = free_dofs




class Analysis:
    # TODO the results of this class needs testing and validation
    # against the MAtlab code
    
    def __init__(self):
        self.stiffness_global_matrix = None
        self.displacement_new_vector = None
        self.force_global_vector = None
        self.transformation_new_matrix = None

    def get_global_stiffness_matrix(self, mesh:Mesh):
        number_nodes = mesh.number_nodes
        number_elements = mesh.number_elements
        node_coordinates = mesh.node_coordinates
        element_connectivity = mesh.element_connectivity
        material_e = mesh.young_modulus
        material_a = mesh.area

        k_global = np.zeros((2 * number_nodes, 2 * number_nodes))

        for i in range(number_elements):
            # Element nodes
            node1, node2 = element_connectivity[i]
            # Element DOFs
            element_dofs = [2 * node1 - 1, 2 * node1, 2 * node2 - 1, 2 * node2]
            # Element material constants
            e = material_e[i]
            a = material_a[i]
            # Element components and length
            dx = node_coordinates[node2-1][0] - node_coordinates[node1-1][0]
            dy = node_coordinates[node2-1][1] - node_coordinates[node1-1][1]
            l = np.sqrt(dx**2 + dy**2)
            # Sine and cosine of angle between reference frames
            c = dx / l
            s = dy / l
            # Global element stiffness matrix
            ke = e * a / l * np.array([
                [c * c, c * s, -c * c, -c * s],
                [c * s, s * s, -c * s, -s * s],
                [-c * c, -c * s, c * c, c * s],
                [-c * s, -s * s, c * s, s * s]
            ])
            # Assembly
            for row_index, dof_i in enumerate(element_dofs):
                for col_index, dof_j in enumerate(element_dofs):
                    k_global[dof_i - 1, dof_j - 1] += ke[row_index, col_index]

        self.stiffness_global_matrix = k_global
        

    def get_global_force_vector(self, forces, dofs):
        number_forces = forces.number_forces
        force_nodes = forces.force_nodes
        force_components = forces.force_components
        force_angles = forces.force_angles
        number_dofs = dofs.number_dofs

        f_global = np.zeros(number_dofs)

        for i in range(number_forces):
            f_node = force_nodes[i]
            f_node_dofs = [2 * f_node - 1, 2 * f_node]
            f_comp_xi_yi = np.array(force_components[i])
            f_angle = force_angles[i]
            c = np.cos(np.radians(f_angle))
            s = np.sin(np.radians(f_angle))
            t = np.array([[c, s], [-s, c]])
            f_comp_xy = t.T @ f_comp_xi_yi
            f_global[f_node_dofs[0] - 1] += f_comp_xy[0]
            f_global[f_node_dofs[1] - 1] += f_comp_xy[1]

        self.force_global_vector = f_global


    def get_new_displacement_vector(self, displacements, dofs):
        """Generate a new displacement vector with the known displacements
        
        #TODO : I don't have a test use case for this method yet
        # currently most displacement would be zeros

        Args:
            displacements (_type_): _description_
            dofs (_type_): _description_
        """
        number_dofs = dofs.number_dofs
        number_pin = displacements.number_pin
        pin_nodes = displacements.pin_nodes
        pin_displacements = displacements.pin_displacements
        pin_angles = displacements.pin_angles
        number_roller = displacements.number_roller
        roller_nodes = displacements.roller_nodes
        roller_directions = displacements.roller_directions
        roller_displacements = displacements.roller_displacements

        uc = np.zeros(number_dofs)

        for i in range(number_pin):
            p_node = pin_nodes[i]
            p_dofs = [2 * p_node - 1, 2 * p_node]
            p_displ_xi_yi = np.array(pin_displacements[i])
            p_angle = pin_angles[i]
            c = np.cos(np.radians(p_angle))
            s = np.sin(np.radians(p_angle))
            t = np.array([[c, s], [-s, c]])
            p_displ_xy = t.T @ p_displ_xi_yi
            uc[p_dofs[0] - 1] = p_displ_xy[0]
            uc[p_dofs[1] - 1] = p_displ_xy[1]

        for i in range(number_roller):
            r_node = roller_nodes[i]
            r_direction = roller_directions[i]
            r_displacement = roller_displacements[i]
            r_dof = 2 * r_node if r_direction == 1 else 2 * r_node - 1
            uc[r_dof - 1] = r_displacement

        self.displacement_new_vector = uc


    def get_new_transformation_matrix(self, displacements, dofs):
        number_dofs = dofs.number_dofs
        number_roller = displacements.number_roller
        roller_nodes = displacements.roller_nodes
        roller_angles = displacements.roller_angles

        tc = np.eye(number_dofs)

        for i in range(number_roller):
            r_node = roller_nodes[i]
            r_dofs = [2 * r_node - 1, 2 * r_node]
            r_angle = roller_angles[i]
            c = np.cos(np.radians(r_angle))
            s = np.sin(np.radians(r_angle))
            t = np.array([[c, s], [-s, c]])
            tc[np.ix_(r_dofs, r_dofs)] = t

        self.transformation_new_matrix = tc



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
    # info.get_project_info()
    print(info.project_directory)
    print(info.file_name)        
# %%
fileData = FileData.from_directory(info.project_directory)
# %%
print(fileData.mesh)
print(fileData.displacements)
# %%
# Usage
mesh = Mesh()
mesh.process_mesh(file_data= fileData.mesh)

# Now mesh instance has its attributes set based on file data
# %%
print("Number of nodes: ", mesh.number_nodes)
print("Number of elements: ", mesh.number_elements)
print("Node coordinates: ", mesh.node_coordinates)  
print("Element connectivity: ", mesh.element_connectivity)  
print("Young's modulus: ", mesh.young_modulus)
print("Area: ", mesh.area)

# %%
# Usage
displacements = Displacements()
displacements.process_displacements(file_data= fileData.displacements)

print(f"Number of pin: {displacements.number_pin}")
print(f"Pin nodes: {displacements.pin_nodes}")
print(f"Pin angles: {displacements.pin_angles}")
print(f"Pin displacements: {displacements.pin_displacements}")
print(f"Number of roller: {displacements.number_roller}")
print(f"Roller nodes: {displacements.roller_nodes}")
print(f"Roller directions: {displacements.roller_directions}")
print(f"Roller angles: {displacements.roller_angles}")
print(f"Roller displacements: {displacements.roller_displacements}")
print(f"Number of support: {displacements.number_support}")

# %%
# Usage
forces = Forces()
forces.process_forces(file_data= fileData.forces)
print(f"Number of forces: {forces.number_forces}")
print(f"Force nodes: {forces.force_nodes}")
print(f"Force angles: {forces.force_angles}")
print(f"Force components: {forces.force_components}")

# %%
def write_input_data(info, mesh, displacements, forces):
    project_dir = info.project_directory
    file_name = info.file_name
    new_file_name = f"{file_name}_DATA.dat"
    file_path = f"{project_dir}/{new_file_name}"

    with open(file_path, 'w') as file:
        bar_line = '-' * 40

        # Writing node coordinates
        file.write('     NODE COORDINATES\n')
        file.write(f'{bar_line}\n')
        file.write('NODE       X(M)        Y(M)\n')
        for i, (x, y) in enumerate(mesh.node_coordinates, start=1):
            file.write(f'{i:<4} {x:11.3f} {y:11.3f}\n')
        file.write('\n')

        # Writing elements
        file.write(' ELEMENTS\n')
        file.write(f'{bar_line}\n')
        file.write('EL.  NODE1  NODE2      A(M2)     E(PA)\n')
        for i, ((node1, node2), a, e) in enumerate(zip(mesh.element_connectivity, mesh.area, mesh.young_modulus), start=1):
            file.write(f'{i:<3} {node1:<6} {node2:<6} {a:11.6G} {e:10.5G}\n')
        file.write('\n')

        # Writing pin supports
        if displacements.number_pin > 0:
            file.write('  PIN SUPPORTS\n')
            file.write(f'{bar_line}\n')
            file.write('NODE    DX\'(M)    DY\'(M)   ANGLE(DEG)\n')
            for node, (dx, dy), angle in zip(displacements.pin_nodes, displacements.pin_displacements, displacements.pin_angles):
                file.write(f'{node:<4} {dx:11.3f} {dy:11.3f} {angle:11.2f}\n')
            file.write('\n')

        # Writing roller supports
        if displacements.number_roller > 0:
            file.write('ROLLER SUPPORTS\n')
            file.write(f'{bar_line}\n')
            file.write('NODE   DIRECTION   DN(M)   ANGLE(DEG)\n')
            for node, direction, dn, angle in zip(displacements.roller_nodes, displacements.roller_directions, displacements.roller_displacements, displacements.roller_angles):
                file.write(f'{node:<4} {direction:<11} {dn:11.3f} {angle:11.2f}\n')
            file.write('\n')

        # Writing forces
        file.write(' FORCES\n')
        file.write(f'{bar_line}\n')
        file.write('NODE     FX\'(N)     FY\'(N)   ANGLE(DEG)\n')
        for node, (fx, fy), angle in zip(forces.force_nodes, forces.force_components, forces.force_angles):
            file.write(f'{node:<4} {fx:11.6G} {fy:11.6G} {angle:11.2f}\n')

# Usage example
# Assume info, mesh, displacements, and forces are instances of their respective classes with attributes set
write_input_data(info=info, mesh=mesh, displacements=displacements, forces=forces)

# %%

# Usage
dofs = Dofs()
# Assume mesh and displacements are instances of their respective classes with attributes set
dofs.process_dofs(mesh=mesh, displacements=displacements)
print(f"Number of DOFs: {dofs.number_dofs}")
print(f"Number of fixed DOFs: {dofs.number_fixed}")
print(f"Number of free DOFs: {dofs.number_free}")
print(f"Fixed DOFs: {dofs.fixed_dofs}")
print(f"Free DOFs: {dofs.free_dofs}")

# %%
# Usage
analysis = Analysis()
# Assume mesh is an instance of the Mesh class with attributes set
analysis.get_global_stiffness_matrix(mesh=mesh)
analysis.get_global_force_vector(forces=forces, dofs=dofs)
print(analysis.stiffness_global_matrix)
print(analysis.stiffness_global_matrix.shape)
print(analysis.stiffness_global_matrix.dtype)
# %%
print(analysis.force_global_vector)
print(analysis.force_global_vector.shape)
print(analysis.force_global_vector.dtype)
# %%
analysis.get_new_displacement_vector(displacements=displacements, dofs=dofs)
print("New Displacement vector==============================")
print(analysis.displacement_new_vector)
print(analysis.displacement_new_vector.shape)
# %%
analysis.get_new_transformation_matrix(displacements=displacements, dofs=dofs)  
print("New Transformation matrix==============================")
print(analysis.transformation_new_matrix)
print(f"New Transformation matrix shape: {analysis.transformation_new_matrix.shape}")
print(f"New Transformation matrix dtype: {analysis.transformation_new_matrix.dtype}")   

# %%
# Usage
solution = Solution()
# Assume analysis and dofs are instances of their respective classes with attributes set
solution.solve_displacement(analysis, dofs)
print("Displacements==============================")
print(solution.new_displacements)
print(solution.new_displacements.shape)
print(solution.new_displacements.dtype)

# %%
