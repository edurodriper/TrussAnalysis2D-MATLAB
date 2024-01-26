import numpy as np
import tkinter as tk
from tkinter import filedialog
import csv
import pathlib

import logging
logging.basicConfig(level=logging.DEBUG)
def read_file(file_name, file_path):
    file_data = []

    with open(file_path / file_name, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each value in the row from string to float
            numeric_row = [float(value) for value in row]
            file_data.append(numeric_row)

    return file_data

class Info:
    def __init__(self, project_directory:str=None, file_name:str=None):
        self.project_directory = project_directory
        self.file_name = file_name

    def get_project_info(self):
        # Set up the root Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Graphical directory selection
        project_dir = filedialog.askdirectory(title='Select Project Folder')
        self.project_directory = project_dir

        # Console input for file name
        file_name = input('Output files name: ')
        self.file_name = file_name

class FileData:
    def __init__(self, mesh=None, displacements=None, forces=None):
        self.mesh = mesh
        self.displacements = displacements
        self.forces = forces

    @staticmethod
    def read_file_text(file_path):
        return file_path.read_text()

    @staticmethod
    def read_file(file_path:pathlib.Path):
        file_data = []
        logging.debug(f'Reading file: {file_path.absolute()}')
        with open(str(file_path.absolute()), mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                logging.debug(f'Reading row: {row}')
                # Convert each value in the row from string to float
                numeric_row = [float(value) for value in row]
                file_data.append(numeric_row)

        return file_data

    @classmethod
    def from_directory(cls, directory):
        directory_path = pathlib.Path(directory)

        # Initialize file paths as None
        mesh_path = displacements_path = forces_path = None

        # Search for specific files in the directory
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                if 'mesh' in file_path.name:
                    logging.debug(f'Found MESH file: {directory_path/file_path.name}')
                    mesh_path = directory_path/file_path
                elif 'displacements' in file_path.name:
                    logging.debug(f'Found DISPLACEMENTS file: {directory_path/file_path.name}')
                    displacements_path = directory_path/file_path
                elif 'forces' in file_path.name:
                    logging.debug(f'Found FORCES file: {directory_path/file_path.name}')
                    forces_path = directory_path/file_path

        # Read the contents of the files, if found
        mesh = cls.read_file(mesh_path) if mesh_path else None
        displacements = cls.read_file(displacements_path) if displacements_path else None
        forces = cls.read_file(forces_path) if forces_path else None

        # Return an instance of FileData with the contents
        return cls(mesh, displacements, forces)

class Mesh:
    def __init__(self):
        self.number_nodes = None
        self.number_elements = None
        self.node_coordinates = None
        self.element_connectivity = None
        self.young_modulus = None
        self.area = None

    def process_mesh(self, file_data:np.ndarray):
        file_line = 0

        # Process node data
        self.number_nodes = int(file_data[file_line][0])
        file_line += 1
        self.node_coordinates = []
        for _ in range(self.number_nodes):
            self.node_coordinates.append((file_data[file_line][0], file_data[file_line][1]))
            file_line += 1

        # Process element data
        self.number_elements = int(file_data[file_line][0])
        file_line += 1
        self.element_connectivity = []
        element_material = []
        for _ in range(self.number_elements):
            self.element_connectivity.append((int(file_data[file_line][0]), int(file_data[file_line][1])))
            element_material.append(int(file_data[file_line][2]))
            file_line += 1

        # Process material data
        number_materials = int(file_data[file_line][0])
        file_line += 1
        material_e = []
        material_a = []
        for _ in range(number_materials):
            material_e.append(file_data[file_line][0])
            material_a.append(file_data[file_line][1])
            file_line += 1

        # Assigning Young's modulus and area to elements
        self.young_modulus = [material_e[mat - 1] for mat in element_material]
        self.area = [material_a[mat - 1] for mat in element_material]


class Displacements:
    def __init__(self):
        self.number_pin = None
        self.pin_nodes = None
        self.pin_displacements = None
        self.pin_angles = None
        self.number_roller = None
        self.roller_nodes = None
        self.roller_directions = None
        self.roller_angles = None
        self.roller_displacements = None
        self.number_support = None
        self.support_nodes = None

    def process_displacements(self, file_data):
        file_line = 0

        # Process pin data
        self.number_pin = int(file_data[file_line][0])
        file_line += 1
        self.pin_nodes = []
        self.pin_angles = []
        self.pin_displacements = []
        for _ in range(self.number_pin):
            self.pin_nodes.append(int(file_data[file_line][0]))
            self.pin_angles.append(file_data[file_line][1])
            self.pin_displacements.append((file_data[file_line][2], file_data[file_line][3]))
            file_line += 1

        # Process roller data
        self.number_roller = int(file_data[file_line][0])
        file_line += 1
        self.roller_nodes = []
        self.roller_directions = []
        self.roller_angles = []
        self.roller_displacements = []
        for _ in range(self.number_roller):
            self.roller_nodes.append(int(file_data[file_line][0]))
            self.roller_directions.append(file_data[file_line][1])
            self.roller_angles.append(file_data[file_line][2])
            self.roller_displacements.append(file_data[file_line][3])
            file_line += 1

        # Process support data
        self.number_support = self.number_pin + self.number_roller
        self.support_nodes = self.pin_nodes + self.roller_nodes



# Now the 'displacements' instance has its attributes set based on the file data


class Forces:
    def __init__(self):
        self.number_forces = None
        self.force_nodes = None
        self.force_components = None
        self.force_angles = None

    def process_forces(self, file_data):
        file_line = 0

        # Process forces data
        self.number_forces = int(file_data[file_line][0])
        file_line += 1
        self.force_nodes = []
        self.force_angles = []
        self.force_components = []
        for _ in range(self.number_forces):
            self.force_nodes.append(int(file_data[file_line][0]))
            self.force_angles.append(file_data[file_line][1])
            self.force_components.append((file_data[file_line][2], file_data[file_line][3],))
            file_line += 1



def write_input_data(info, mesh, displacements, forces):
    """Write input data for the problem to a file	

    Includes mesh, Displacements, and Forces data
    """
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


