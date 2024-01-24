#%%
import tkinter as tk
from tkinter import filedialog
import csv
import pathlib
from truss_input import Info, FileData,Mesh,Displacements,Forces


class Dofs:
    def __init__(self):
        self.number_dofs = None
        self.number_fixed = None
        self.number_free = None
        self.fixed_dofs = None
        self.free_dofs = None

class Analysis:
    def __init__(self):
        self.stiffness_global_matrix = None
        self.displacement_new_vector = None
        self.force_global_vector = None
        self.transformation_new_matrix = None

class Solution:
    def __init__(self):
        self.new_displacements = None
        self.new_forces = None
        self.global_displacements = None
        self.global_forces = None
        self.global_reactions = None
        self.element_stress = None
        self.element_force = None

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
