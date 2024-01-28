#%%
import pathlib
import numpy as np
import tkinter as tk
from tkinter import filedialog

from npp_2d_truss_analysis.truss_input import Info, FileData,Mesh,Displacements,Forces, write_input_data
from npp_2d_truss_analysis.truss_analysis_2d import Dofs, Analysis

class Solution:
    def __init__(self):
        self.new_displacements = None
        self.new_forces = None
        self.global_displacements = None
        self.global_forces = None
        self.global_reactions = None
        self.element_stress = None
        self.element_force = None

    def solve_displacement(self, analysis:Analysis, dofs:Dofs):
        fixed_dofs = (np.array([dofs.fixed_dofs])-1).flatten()
        free_dofs = (np.array([dofs.free_dofs])-1).flatten()
        f = analysis.force_global_vector
        uc = analysis.displacement_new_vector
        tc = analysis.transformation_new_matrix
        k = analysis.stiffness_global_matrix

        # New force vector
        fc = tc @ f
        # New stiffness matrix
        kc = tc @ k @ tc.T

        # Free new displacements
        # uc[free_dofs] = np.linalg.solve(kc[np.ix_(free_dofs, free_dofs)], 
        #             fc[free_dofs] - kc[np.ix_(free_dofs, fixed_dofs)] @ uc[fixed_dofs])
        uc[free_dofs] = np.linalg.inv(kc[np.ix_(free_dofs, free_dofs)])@ fc[free_dofs] - kc[np.ix_(free_dofs, fixed_dofs)] @ uc[fixed_dofs]


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


    def solve_reaction(self, displacements:Displacements):
        """returns the global reactions in a 2x(number of supports) array

        row 1 : x component
        row 2 : y component

        Starts with pin

        Args:
            displacements(Displacements): Container with the displacements data
        returns

            self.global_reactions (ndarray[2x(number of supports)]): global reactions.
        """        
        fc = self.new_forces
        number_pin = displacements.number_pin
        pin_nodes = displacements.pin_nodes
        number_roller = displacements.number_roller
        roller_nodes = displacements.roller_nodes
        roller_directions = displacements.roller_directions
        roller_angles = displacements.roller_angles
        number_support = displacements.number_support

        r = np.zeros((2, number_support))
        s_node = 0

        # Pin support
        for i in range(number_pin):
            p_node = pin_nodes[i]
            fixed_dofs = [2 * (p_node-1) , 2 * (p_node-1)+1]
            r[:, s_node] = fc[fixed_dofs]
            # print(f"{r[:, s_node] }")
            s_node += 1

        # Roller support
        for i in range(number_roller):
            r_node = roller_nodes[i]-1
            r_direction = roller_directions[i]
            r_angle = roller_angles[i]
            rc = np.zeros(2)
            if r_direction == 1:
                # fixes the normal direction, allows rolling on x
                fixed_dof = 2 * r_node+1
                rc[1] = fc[fixed_dof]
            else:
                # r_direction ==2 fixes the horizontal direction
                fixed_dof = 2 * r_node
                rc[0] = fc[fixed_dof]
            
            c = np.cos(np.radians(r_angle))
            s = np.sin(np.radians(r_angle))
            rot = np.array([[c, s], [-s, c]])
            r[:, s_node] = rot.T @ rc
            # logging.debug(f"{r[:, s_node] }")
            s_node += 1

        self.global_reactions = r
        return  self.global_reactions

    def solve_stress(self, mesh:Mesh):
        u = self.global_displacements
        number_elements = mesh.number_elements
        node_coordinates = mesh.node_coordinates
        element_connectivity = mesh.element_connectivity
        material_e = mesh.young_modulus
        material_a = mesh.area

        element_stress = np.zeros(number_elements)
        element_force = np.zeros(number_elements)

        for i in range(number_elements):
            # Element nodes
            node1, node2 = element_connectivity[i]
            # Element DOFs
            element_dofs = [2 * (node1 - 1), 2 * (node1-1)+1, 2 * (node2 - 1), 2 *( node2-1)+1]
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
            # Element transformation matrix
            t = np.array([[c, s, 0, 0], [-s, c, 0, 0], [0, 0, c, s], [0, 0, -s, c]])
            # Local element displacements
            ul = t @ u[element_dofs]
            # Element stress
            element_stress[i] = e * 1 / l * np.array([-1, 0, 1, 0]) @ ul
            # Element force
            element_force[i] = element_stress[i] * a

        self.element_stress = element_stress
        self.element_force = element_force


    def get_max_displacement(self)->float:
        """Returns the maximum displacement

        convenience method to obtain the maximum displacement for the paper size. 

        Returns:
            float: maximum displacement or 0 if no displacements are available
        """
        try:
            u = self.global_displacements
            return np.max(np.abs(u))
        except (TypeError, AttributeError):
            return 0

    def report_displacements(self, mesh:Mesh)->str:
        """Returns a string with the displacements report

        #TODO  Do the same for reactions and stresses

        Returns:
            str: displacements report
        """      
        number_nodes = mesh.number_nodes
        u = self.global_displacements
        r = self.global_reactions
    
        bar_line = '-' * 40  
        ret_str='   NODE DISPLACEMENTS\n'
        ret_str +=(f'{bar_line}\n')
        ret_str +=('NODE       DX(M)        DY(M)        DM(M)\n')
        for i in range(number_nodes):
            displ_x = u[2*i]
            displ_y = u[2*i + 1]
            displ_m = (displ_x**2 + displ_y**2)**0.5
            ret_str+=(f'{i+1:<4} {displ_x:11.3E} {displ_y:11.3E} {displ_m:11.3E}\n')
        return ret_str

def write_results(info, mesh:Mesh, displacements:Displacements, solution:Solution):
    project_dir = info.project_directory
    file_name = info.file_name
    number_nodes = mesh.number_nodes
    number_elements = mesh.number_elements
    number_support = displacements.number_support
    support_nodes = displacements.support_nodes
    u = solution.global_displacements
    r = solution.global_reactions
    element_stress = solution.element_stress
    element_force = solution.element_force

    new_file_name = f"{file_name}_RESULTS.dat"
    file_path = f"{project_dir}/{new_file_name}"

    with open(file_path, 'w') as file:
        bar_line = '-' * 40

        # Writing node displacements
        file.write('   NODE DISPLACEMENTS\n')
        file.write(f'{bar_line}\n')
        file.write('NODE       DX(M)        DY(M)        DM(M)\n')
        for i in range(number_nodes):
            displ_x = u[2*i]
            displ_y = u[2*i + 1]
            displ_m = (displ_x**2 + displ_y**2)**0.5
            file.write(f'{i+1:<4} {displ_x:11.3E} {displ_y:11.3E} {displ_m:11.3E}\n')
        file.write('\n')

        # Writing element forces and stresses
        file.write('  ELEMENT FORCES AND STRESSES\n')
        file.write(f'{bar_line}\n')
        file.write('EL.       FORCE(N)       STRESS(PA)\n')
        for i in range(number_elements):
            elem_force = element_force[i]
            elem_stress = element_stress[i]
            file.write(f'{i+1:<3} {elem_force:+14.6E} {elem_stress:+14.6E}\n')
        file.write('\n')

        # Writing support reactions
        file.write('  SUPPORT REACTIONS\n')
        file.write(f'{bar_line}\n')
        file.write('NODE       RX(N)        RY(N)        RM(N)\n')
        for i in range(number_support):
            s_node = support_nodes[i]
            react_x = r[0, i]
            react_y = r[1, i]
            react_m = (react_x**2 + react_y**2)**0.5
            file.write(f'{s_node:<4} {react_x:11.3E} {react_y:11.3E} {react_m:11.3E}\n')


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
    #%%
    solution = Solution()
    # Assume analysis and dofs are instances of their respective classes with attributes set
    solution.solve_displacement(analysis, dofs)
    print("Displacements==============================")
    print(solution.new_displacements)
    print(solution.new_displacements.shape)
    print(solution.new_displacements.dtype)
    print(f"Global displacements: {solution.global_displacements}")	
    print(f"New forces: {solution.new_forces}")
    print(f"Global forces: {solution.global_forces}")
    
    # %%
    print("Solve Reactions==================================")	
    solution.solve_reaction(displacements=displacements)
    print(solution.global_reactions)
    print(solution.global_reactions.shape)
    print(solution.global_reactions.dtype)
    
    # %%
    solution.solve_stress(mesh=mesh)
    # Usage example
    # Assume info, mesh, displacements, and solution are instances of their respective classes with attributes set
    write_results(info, mesh=mesh, displacements=displacements, solution=solution)
